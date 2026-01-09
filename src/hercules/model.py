# hercules/model.py
import joblib
from proteinbert import OutputType, OutputSpec, FinetuningModelGenerator, load_pretrained_model
from proteinbert.conv_and_global_attention_model import get_model_with_hidden_layers_as_outputs
from importlib.resources import files

OUTPUT_TYPE = OutputType(False, 'binary')
OUTPUT_SPEC = OutputSpec(OUTPUT_TYPE, [0, 1])

def load_model_generator():
    pretrained_model_generator, input_encoder = load_pretrained_model()

    weights_path = files("hercules.data") / "proteinbert_weights.pkl"
    model_weights = joblib.load(weights_path)

    model_generator = FinetuningModelGenerator(
        pretrained_model_generator,
        OUTPUT_SPEC,
        pretraining_model_manipulation_function=get_model_with_hidden_layers_as_outputs,
        model_weights=model_weights,
        dropout_rate=0.5,
    )
    return model_generator, input_encoder
