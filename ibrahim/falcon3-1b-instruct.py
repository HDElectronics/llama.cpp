from PIL import Image
import requests
import re
import io
from transformers import AutoProcessor, AutoModelForImageTextToText

model_id = "/home/ibrahim/Falcon3-vision-models/Falcon3-Vision-1B-Instruct/"

model = AutoModelForImageTextToText.from_pretrained(model_id, torch_dtype="auto", trust_remote_code=True).to('cuda')

min_pixels = 32 * 28 * 28
max_pixels = 160 * 28 * 28
processor = AutoProcessor.from_pretrained(model_id, min_pixels=min_pixels, max_pixels=max_pixels, trust_remote_code=True)


url = "https://www.minneapolisfed.org/-/media/assets/articles/2024/big-city-higher-pay/big-city-higher-pay-key.jpg"
response = requests.get(url)
image = Image.open(io.BytesIO(response.content))

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
