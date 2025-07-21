from transformers import AutoModelForImageTextToText
import json


model_id = "/home/ibrahim/Falcon3-vision-models/Falcon3-Vision-1B-Instruct/"
model = AutoModelForImageTextToText.from_pretrained(model_id, torch_dtype="auto", trust_remote_code=True).to('cuda')

# Collect all tensor names and shapes
tensor_dict = {name: list(param.shape) for name, param in model.named_parameters()}

# Save to JSON file
with open("ibrahim/tensor_names_shapes_falcon3vl.json", "w") as f:
    json.dump(tensor_dict, f, indent=2)

# Optionally, print the dict
for name, shape in tensor_dict.items():
    print(f"{name}: {shape}")
