from transformers import pipeline
from transformers import AutoTokenizer, AutoModel, AutoModelForSequenceClassification, TFAutoModel, TFAutoModelForSequenceClassification
import torch
import tensorflow as tf

classifier = pipeline("sentiment-analysis")
checkpoint = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
pytorch_model = AutoModel.from_pretrained(checkpoint)
tensorflow_model = TFAutoModel.from_pretrained(checkpoint)
pytorch_sequence_model = AutoModelForSequenceClassification.from_pretrained(checkpoint)
tensorflow_sequence_model = TFAutoModelForSequenceClassification.from_pretrained(checkpoint)

# Raw input 
raw_inputs = [
"I am not having the best of my days",
"Things are actually a bit frustrating but I am positive I will die some day"
]

# Generate tokenized input
pytorch_inputs = tokenizer(raw_inputs, padding=True, truncation=True, return_tensors="pt") # return_tensors="pt" is needed for PyTorch
tensorflow_inputs = tokenizer(raw_inputs, padding=True, truncation=True, return_tensors="tf") # return_tensors="tf" is needed for TensorFlow

# Generate outputs
pytorch_outputs = pytorch_model(**pytorch_inputs)
tensorflow_outputs = tensorflow_model(**tensorflow_inputs)
pytorch_sequence_outputs = pytorch_sequence_model(**pytorch_inputs)
tensorflow_sequence_outputs = tensorflow_sequence_model(**tensorflow_inputs)
torch_predictions = torch.nn.functional.softmax(pytorch_sequence_outputs.logits, dim=-1)
tensorflow_predictions = tf.nn.softmax(tensorflow_sequence_outputs.logits, axis=-1)

# Sentiment analysis
print(f"Classifier prediction with pipeline API: {classifier(raw_inputs)}")
print(f"Tokenized pytorch inputs: {pytorch_inputs}")
print(f"Tokenized tensorflow inputs: {tensorflow_inputs}")
print(f"Shape of last hidden state from pre-trained distilbert pytorch: {pytorch_outputs.last_hidden_state.shape}")
print(f"Shape of last hidden state from pre-trained distilbert tensorflow: {tensorflow_outputs.last_hidden_state.shape}")
print(f"Logits shape generated by sequence model pytorch: {pytorch_sequence_outputs.logits.shape}")
print(f"Logits shape generated by sequence model tensorflow: {tensorflow_sequence_outputs.logits.shape}")
print(f"Logits generated by sequence model pytorch: {pytorch_sequence_outputs.logits}")
print(f"Logits generated by sequence model tensorflow: {tensorflow_sequence_outputs.logits}")
print(f"Predictions generated by pytorch: {torch_predictions}")
print(f"Predictions generated by tensorflow: {tensorflow_predictions}")
print(f"Labels ID used in sequence model pytorch: {pytorch_sequence_model.config.label2id}")
print(f"Labels ID used in sequence model tensorflow: {tensorflow_sequence_model.config.label2id}")