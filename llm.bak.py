# curl http://localhost:11434/v1/chat/completions \
#     -H "Content-Type: application/json" \
#     -d '{
#         "model": "llama2",
#         "messages": [
#             {
#                 "role": "system",
#                 "content": "You are a helpful assistant."
#             },
#             {
#                 "role": "user",
#                 "content": "Hello!"
#             }
#         ]
#     }'

import requests

def api(messages, model):
    url = "http://localhost:11434/v1/chat/completions"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "model": "ibm-granite/granite-8b-code-instruct-128k",
        "messages": messages
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

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
    model = "ibm-granite/granite-8b-code-instruct-128k"
    response = api(messages, model)
    print(response)