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

def calculate_attentions(model, input_encoder, seq):
    seq_len = len(seq) + 2
    X = input_encoder.encode_X([seq], seq_len)
    (X_seq,), _ = X

    model_inputs = [l.input for l in model.layers if "InputLayer" in str(type(l))][::-1]
    model_attentions = [
        l.calculate_attention(l.input)
        for l in model.layers
        if "GlobalAttention" in str(type(l))
    ]

    fn = K.function(model_inputs, model_attentions)
    att = fn(X)
    merged = np.concatenate([head for layer in att for head in layer]) if att else np.zeros((len(seq), 1))
    return np.mean(merged, axis=0)[1:-1] if merged.ndim > 1 else merged
    #merged = np.concatenate([head for layer in att for head in layer])
    #return np.mean(merged, axis=0)[1:-1]
