import os
import openai
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are an expert in algorithms and data strucutres."},
    {"role": "user", "content": "What is breadth-first search?."}
  ]
)

print(completion.choices[0].message["content"])