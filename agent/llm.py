import http.client
import json
import re

def prompt_create_index(path_base, directory_contents):
    paths = [f"[{path}]({path_base}/{path})" for path in directory_contents]
    prompt = "\n".join(
        [
            "# instruction",
            "create an index.md markdown file",
            "the file only serves to nicely display the following paths:",
            "\n".join(paths),
            "use markdown links with this pattern []() to link to the files",
            "group and illustrate the files in different ways and provide a brief description",
        ]
    )
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
    return messages


def api(messages, model):
    conn = http.client.HTTPConnection("localhost", 11434)
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": messages
    }
    
    json_data = json.dumps(data)
    
    conn.request("POST", "/v1/chat/completions", body=json_data, headers=headers)
    
    response = conn.getresponse()
    response_data = response.read().decode("utf-8")

#     return f"""# prompt
# ## messages
# {json.dumps(messages, indent=4)}
# ## response
# {json.loads(response_data)["choices"][0]["message"]["content"]}"""
    lines = [
        "# prompt",
        "## messages",
        json.dumps(messages, indent=4),
        "## response",
        json.loads(response_data)["choices"][0]["message"]["content"]
    ]
    return "\n".join(lines)

if __name__ == "__main__":
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "Hello!"
        }
    ]
    model = "granite-code:3b"
    response = api(messages, model)
    print(response)

    import os
    listdir_result = os.listdir()

    messages = prompt_create_index("agent", listdir_result)
    response = api(messages, model)
    print(response)