import os
import requests
from anthropic import Anthropic, APIError
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def call_anthropic(prompt):
    try:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text
    except APIError as e:
        return f"[ERROR] Anthropic API call failed: {e}"
    except Exception as e:
        return f"[ERROR] Unexpected error in call_anthropic: {e}"
    

def call_ollama(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gemma3:4b",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.ConnectionError:
        return "[ERROR] Ollama is not running. Start it with 'ollama serve'."
    except requests.exceptions.Timeout:
        return "[ERROR] Ollama did not respond within 60 seconds."
    except Exception as e:
        return f"[ERROR] Unexpected error in call_ollama: {e}"
    
def call_llm(prompt, provider="anthropic"):
    if provider == "anthropic":
        return call_anthropic(prompt)
    elif provider == "ollama":
        return call_ollama(prompt)
    else:
        raise ValueError(f"Unknown provider: {provider}")
    

if __name__ == "__main__":
    print("--- Anthropic ---")
    print(call_anthropic("Say hello in one short sentence."))
    print("\n--- Ollama ---")
    print(call_ollama("Say hello in one short sentence."))
    print("\n--- call_llm with default (anthropic) ---")
    print(call_llm("Say hello in one short sentence."))
    print("\n--- call_llm with explicit ollama ---")
    print(call_llm("Say hello in one short sentence.", provider="ollama"))