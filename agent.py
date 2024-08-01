import ollama

HOST_OLLAMA="http://localhost:11434"

ollama_client = ollama.Client(host=HOST_OLLAMA)

def construct_prompt(
    pre_prompt: str,
    prompt: str,
    post_prompt: str
) -> str:
    # name this pattern
    return [
        "# prompts",
        "## pre_prompt",
        "{pre_prompt}",
        "## prompt",
        "{prompt}",
        "## post_prompt",
        "{post_prompt}",
        "# prompts"
    ]

def generate(prompt: str):
    ollama.generate(prompt)

if __name__ == "__main__":
    pre_prompt = "you are a researcher"
    prompt = "you are disecting a lithium ion cell"
    post_prompt = "what do you see?"

    prompt = construct_prompt(pre_prompt, prompt, post_prompt)