import os
import json
import time
from openai import OpenAI
from openai import RateLimitError

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MAX_RETRIES = 3
BACKOFF_SECONDS = 6
MAX_INPUT_CHARS = 12000  # hard guardrail

def _truncate(text: str) -> str:
    if len(text) <= MAX_INPUT_CHARS:
        return text
    return text[:MAX_INPUT_CHARS] + "\n\n[TRUNCATED DUE TO TOKEN LIMITS]"

def call_llm(prompt: str):
    safe_prompt = _truncate(prompt)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.responses.create(
                model="gpt-4.1-mini",
                input=safe_prompt,
                temperature=0
            )

            text = response.output_text or ""

            try:
                return json.loads(text)
            except Exception:
                return {
                    "summary": "\n".join(text.splitlines()[:6]),
                    "critical_issues": [],
                    "recommendations": []
                }

        except RateLimitError as e:
            if attempt == MAX_RETRIES:
                break
            time.sleep(BACKOFF_SECONDS * attempt)

        except Exception as e:
            return {
                "summary": "LLM invocation failed",
                "critical_issues": [str(e)],
                "recommendations": ["Check OpenAI configuration or reduce prompt size"]
            }

    # Final safe fallback (PIPELINE MUST NOT FAIL)
    return {
        "summary": "LLM rate-limited. Static analysis completed successfully.",
        "critical_issues": [],
        "recommendations": [
            "Re-run workflow after cooldown",
            "Reduce analyzer verbosity",
            "Split analysis by language"
        ]
    }
