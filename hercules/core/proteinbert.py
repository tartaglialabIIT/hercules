# hercules/proteinbert.py
from typing import List
import numpy as np
import pandas as pd
from tensorflow.keras import backend as K
from proteinbert.tokenization import index_to_token
from proteinbert.finetuning import encode_dataset

def proteinbert_global_score(
    sequences: List[str],
    model_generator,
    input_encoder,
    output_spec,
    batch_size=32
) -> np.ndarray:
    """
    Returns y_pred for each sequence
    """
    X, _, sample_weights = encode_dataset(
        sequences,
        pd.Series([0] * len(sequences)),
        input_encoder,
        output_spec,
        seq_len=max(len(s) for s in sequences) + 2,
        needs_filtering=False
    )

    model = model_generator.create_model(X[0].shape[1])
    y_pred = model.predict(X, batch_size=batch_size).flatten()
    return y_pred

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
