import os
from types import NoneType

from openai import OpenAI

client = OpenAI(
#    base_url = "https://integrate.api.nvidia.com/v1",
#    api_key = "???"
)

def infer(instruct:NoneType|str, prompt:str):
    messages = []
    if instruct:
        messages.append({"role": "system", "content": instruct})
    messages.append({"role": "user", "content": prompt})
    completion = client.chat.completions.create(
        model=os.environ["LLM"], # "meta/llama3-70b-instruct",
        messages=messages,
        temperature=0.1,
        top_p=1,
        max_tokens=1024,
        stream=False
    )
    return completion.choices[0].message.content

