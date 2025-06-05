import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    base_url="https://api.cometapi.com/v1",
    api_key=os.getenv("COMET_API_KEY"),    
)

response = client.chat.completions.create(
    model="o4-mini",
    messages=[
        {
            "role": "system",
            "content": "eres un asistente de aprendizaje de ingles transicional, de español a ingles, guia al alumno en su ruta de manera activa y amble",
        },
        {
            "role": "user",
            "content": "hola que tal"
        },
    ],
)

message = response.choices[0].message.content

print(f"Assistant: {message}")