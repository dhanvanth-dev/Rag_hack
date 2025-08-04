import httpx
import asyncio

OPENROUTER_API_KEY = "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"

async def call_deepseek_r1(prompt: str)-> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "deepseek/deepseek-r1-0528:free",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = httpx.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body, timeout=20)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {e}"
