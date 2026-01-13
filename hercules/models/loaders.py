# hercules/models/loaders.py
import joblib
from proteinbert import OutputType, OutputSpec, FinetuningModelGenerator, load_pretrained_model
from proteinbert.conv_and_global_attention_model import get_model_with_hidden_layers_as_outputs
#from importlib.resources import files

try:
    # Python ≥ 3.9
    from importlib.resources import files
except ImportError:
    # Python 3.8
    from importlib_resources import files

OUTPUT_TYPE = OutputType(False, 'binary')
OUTPUT_SPEC = OutputSpec(OUTPUT_TYPE, [0, 1])

import torch
from .fusion_nn import FusionNN

def load_fusion_model():
    # Load the checkpoint
    path = files("hercules.models.weights") / "fusion_nn.pt"
    checkpoint = torch.load(path, map_location="cpu")

    # Extract the binary_task flag
    binary_task = checkpoint.get("binary_task", False)

    # Recreate the model architecture with the same binary_task
    model = FusionNN(binary_task=binary_task)

    # Load the actual weights
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    return model

def load_model_generator():
    pretrained_model_generator, input_encoder = load_pretrained_model()

    weights_path = files("hercules.models.weights") / "proteinbert_weights.pkl"
    model_weights = joblib.load(weights_path)

    model_generator = FinetuningModelGenerator(
        pretrained_model_generator,
        OUTPUT_SPEC,
        pretraining_model_manipulation_function=get_model_with_hidden_layers_as_outputs,
        model_weights=model_weights,
        dropout_rate=0.5,
    )
    return model_generator, input_encoder, OUTPUT_SPEC
