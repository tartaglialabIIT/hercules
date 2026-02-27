# hercules/proteinbert.py
from typing import List
import numpy as np
import pandas as pd
from tensorflow.keras import backend as K
from proteinbert.tokenization import index_to_token
from proteinbert.finetuning import encode_dataset,split_dataset_by_len

def proteinbert_global_score(
    sequences: List[str],
    model_generator,
    input_encoder,
    output_spec,
    start_seq_len=512,
    start_batch_size=32,
    increase_factor=2,
) -> np.ndarray:
    """
    Returns y_pred for each sequence
    """
    dataset = pd.DataFrame({"seq": sequences})
    dataset["orig_index"] = np.arange(len(dataset))

    y_pred_ordered = np.full(len(dataset), np.nan, dtype=np.float32)

    for len_matching_dataset, seq_len, batch_size in split_dataset_by_len(
        dataset,
        start_seq_len=start_seq_len,
        start_batch_size=start_batch_size,
        increase_factor=increase_factor,
    ):
        orig_idx = len_matching_dataset["orig_index"].values

        X, _, sample_weights = encode_dataset(
            len_matching_dataset["seq"],
            pd.Series([0] * len(len_matching_dataset)),
            input_encoder,
            output_spec,
            seq_len=seq_len,
            needs_filtering=False,
        )

        y_mask = (sample_weights == 1)
        n_valid = int(np.sum(y_mask))

        # ✅ If this bucket has no valid samples, skip it (don’t call predict)
        if n_valid == 0:
            continue

        model = model_generator.create_model(seq_len)

        # ✅ Robust inference; avoids some predict() empty-step edge cases
        y_pred = model(X, training=False).numpy().reshape(-1)

        # Fill only valid ones back into global vector
        y_pred_ordered[orig_idx[y_mask]] = y_pred[y_mask]

    # If anything is still NaN, those sequences never produced valid samples
    if np.isnan(y_pred_ordered).any():
        missing = np.where(np.isnan(y_pred_ordered))[0]
        raise ValueError(
            f"{len(missing)} sequences produced no valid ProteinBERT encoding "
            f"(sample_weights==0 in all buckets). First missing indices: {missing[:10]}"
        )

    return y_pred_ordered

def calculate_attentions(model, input_encoder, seq, seq_len):
    X = input_encoder.encode_X([seq], seq_len)
    (X_seq,), _ = X

    model_inputs = [
        l.input for l in model.layers
        if "InputLayer" in str(type(l))
    ][::-1]

    model_attentions = [
        l.calculate_attention(l.input)
        for l in model.layers
        if "GlobalAttention" in str(type(l))
    ]

    invoke_model_attentions = K.function(model_inputs, model_attentions)
    attention_values = invoke_model_attentions(X)

    merged_attention_values = []
    for layer_vals in attention_values:
        for head_vals in layer_vals:
            merged_attention_values.append(head_vals)

    attention_values = np.array(merged_attention_values)

    # tokens (ProteinBERT convention)
    seq_tokens = ["<START>"] + list(seq) + ["<END>"]

    return attention_values, seq_tokens

def get_attention_profile(
    seq: str,
    model_generator,
    input_encoder
) -> np.ndarray:
    """
    Returns per-residue attention profile of shape (L,)
    """
    seq_len = len(seq) + 2
    model = model_generator.create_model(seq_len)

    attention_values, seq_tokens = calculate_attentions(
        model,
        input_encoder,
        seq,
        seq_len
    )

    # attention_values shape: (n_heads * n_layers, seq_len)
    profile = np.mean(attention_values, axis=0)

    # remove <START> and <END>
    return profile[1:-1]
