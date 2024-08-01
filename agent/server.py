from fastapi.routing import APIRouter
import llm
import os
import uuid

ID = os.environ.get("ID", str(uuid.uuid4()))

router = APIRouter()

indexHTML = """
<!DOCTYPE html>
<html>
    <head>
        <title>Agent</title>
    </head>
    <body>
        <h1>Agent</h1>
        <p>Agent is a helpful assistant.</p>
    </body>
</html>
"""

@router.get("/")
async def index():
    return indexHTML


def create_index():
    files = os.listdir()
    path_base = ID
    messages = llm.prompt_create_index(path_base, files)
    response = llm.api(messages, "granite-code:3b")
    global indexHTML
    indexHTML = response



if __name__ == "__main__":
    import uvicorn
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(router)
    create_index()
    uvicorn.run(app, host="localhost", port=8000)