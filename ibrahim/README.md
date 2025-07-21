---
license: other
language:
- en
base_model:
- tiiuae/Falcon3-1B-Base
- tiiuae/Falcon3-Vision-1B-Base
library_name: transformers
tags:
- falcon
- falcon_vl
- falcon-vision
---
<img 
    style="display: block; 
           margin-left: auto;
           margin-right: auto;"
    src="https://cdn-uploads.huggingface.co/production/uploads/60d3b119b8448e1785bbda25/qd0Ab1Qj7u5MYEYcni7fa.png" >
</img>

# Falcon3-Vision-1B-Instruct

<!-- Provide a quick summary of what the model is/does. -->
**Falcon3-Vision** family of Open Foundation Models is a set of base and instruct VLMs ranging from 1B to 10B, based on the [**Falcon3-Vision**](https://huggingface.co/collections/tiiuae/falcon3-vision-677d9d6ddb3d83285af57fb0) family of VLMs.

This repository contains the **Falcon3-Vision-1B-Instruct** model. This has been only been trained on image-text conversation data and can be used as a chat model. 

## Model Details
- Base LLM: [**Falcon3-1B-Base**](https://huggingface.co/tiiuae/Falcon3-1B-Base)
- Model Type: Instruct model for image understanding
- LLM Architecture
  - Transformer-based causal decoder-only architecture
  - 18 decoder blocks
  - Grouped Query Attention (GQA) for faster inference: 12 query heads and 4 key-value heads
  - Wider head dimension: 256
  - High RoPE value to support long context understanding: 1000042
  - Uses SwiGLU and RMSNorm
  - 32K context length
  - 131K vocab size
- ViT Architecture:
  - 32 encoder blocks
  - 16 attention heads
  - 1280 hidden dimension
- Support multiple images at variable resolutions and aspect ratios
- Supports EN
- Developed by: [Technology Innovation Institute](https://www.tii.ae/)
- License: TII Falcon-LLM License 2.0
- Model Release Date: January 2025

## Getting Started


<details>
<summary> Click to expand </summary>
  
```python
import torch
from PIL import Image
import requests
import torch
import re
from typing import Dict
from transformers import AutoProcessor, AutoModelForImageTextToText

model_id = "tiiuae/Falcon3-Vision-1B-Instruct"

model = AutoModelForImageTextToText.from_pretrained(model_id, torch_dtype="auto", trust_remote_code=True).to('cuda')
processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)


url = "URL to an image"
image = Image.open(requests.get(url, stream=True).raw)

conversation = [
    {
        "role": "user",
        "content": [
            {
                "type": "image",
            },
            {"type": "text", "text": "Enter the prompt here"},
        ],
    }
]

formatted_prompt = processor.apply_chat_template(conversation, add_generation_prompt=True, tokenize=False)

print(formatted_prompt)

inputs = processor(
    text=[formatted_prompt], images=[image], padding=True, return_tensors="pt"
)
inputs = inputs.to('cuda')

output_ids = model.generate(**inputs, max_new_tokens=2048, eos_token_id=[11])
generated_ids = [output_ids[len(input_ids) :] for input_ids, output_ids in zip(inputs.input_ids, output_ids)]
output_text = processor.batch_decode(
    generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True
)[0]

print('##########################################################################################')
formatted_output = re.sub(r"^(.*?)(?:</thinking>)(.*?)(?:\|<end_of_turn>\|)$", lambda m: f"Analysis:\n{m.group(1).strip()}\n\nFinal Answer:\n{m.group(2).strip()}", output_text)
print(formatted_output)
```

</details>

<br>

## Example
<img src="https://cdn-uploads.huggingface.co/production/uploads/6460e69a933afb0106a8877e/BKYhaEKUkftQ9evwcdd7s.png" width="768"/>


## Useful links
- View our [release blogpost](https://huggingface.co/blog/falcon3-Vision).
- Feel free to join [our discord server](https://discord.gg/fwXpMyGc) if you have any questions or to interact with our researchers and developers.

## Technical Report
Coming soon....

## Citation
If the Falcon3 family of models were helpful to your work, feel free to give us a cite.
 
```
@misc{Falcon3,
    title = {The Falcon 3 Family of Open Models},
    url = {https://huggingface.co/blog/falcon3-vision},
    author = {Falcon-LLM Team},
    month = {January},
    year = {2025}
}