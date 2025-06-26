import os
import asyncio
from fastmcp import FastMCP
import vertexai
vertexai.init(project=os.getenv("GCP_PROJECT"), location="asia-northeast1")
chat_model = vertexai.language_models.ChatModel.from_pretrained("chat-bison")
mcp = FastMCP("Gemini Tool Server")
@mcp.tool()
def generate_reply(prompt: str) -> str:
    chat = chat_model.start_chat()
    resp = chat.send_message(prompt)
    return resp.text
if __name__ == "__main__":
    asyncio.run(mcp.run_async(
        transport="streamable-http", host="0.0.0.0", port=int(os.getenv("PORT", 8080))
    ))
