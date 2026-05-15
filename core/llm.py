# core/llm.py
import ollama
from core.config import cfg
from utils.logger import log


def ask_llm(
    prompt: str, 
    model: str = None, 
    stream: bool = False,
    temperature: float = 0.7,
    top_p: float = 0.9
):
    """
    Send a prompt to an Ollama model with generation options.
    """
    model = model or cfg.ollama_model
    messages = [{"role": "user", "content": prompt}]
    options = {
        "temperature": temperature,
        "top_p": top_p,
    }

    try:
        if stream:
            return ollama.chat(model=model, messages=messages, stream=True, options=options)
        else:
            response = ollama.chat(model=model, messages=messages, options=options)
            return response["message"]["content"]
    except Exception as e:
        log.error(f"LLM call failed (model={model}): {e}")
        raise RuntimeError(
            f"Could not reach Ollama model '{model}'. "
            f"Is Ollama running? Have you pulled the model?\n"
            f"Try: ollama pull {model}"
        ) from e
