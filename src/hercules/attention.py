# hercules/attention.py
import numpy as np
from tensorflow.keras import backend as K
from proteinbert.tokenization import index_to_token

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

    merged = np.concatenate([head for layer in att for head in layer])
    return np.mean(merged, axis=0)[1:-1]
