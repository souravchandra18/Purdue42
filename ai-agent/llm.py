import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_llm(prompt):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        temperature=0
    )

    text = response.output_text
    try:
        return json.loads(text)
    except Exception:
        return {
            "summary": "\n".join(text.splitlines()[:6]),
            "critical_issues": [],
            "recommendations": []
        }
