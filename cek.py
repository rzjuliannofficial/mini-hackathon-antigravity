from google import genai
import os

client = genai.Client(api_key="AIzaSyC93xhfaWy-ablFexJVZzJcXQlkRZ9O21c")

print("Mencari model yang tersedia...\n")
for model in client.models.list():
    print(f"Model: {model.name}")
    print(f"  Full details: {model}")
    print()