import os
import asyncio
import sys
from fastmcp import FastMCP
import vertexai
from vertexai.generative_models import GenerativeModel

try:
    gcp_project = os.getenv("GCP_PROJECT")
    if not gcp_project:
        print("FATAL: GCP_PROJECT environment variable is not set.", file=sys.stderr)
        sys.exit(1)
    
    print(f"Initializing Vertex AI for project: {gcp_project}")
    vertexai.init(project=gcp_project, location="asia-northeast1")
    chat_model = GenerativeModel("gemini-2.0-flash")
    print("Vertex AI initialized successfully.")
except Exception as e:
    print(f"FATAL: Failed to initialize Vertex AI: {e}", file=sys.stderr)
    sys.exit(1)

mcp = FastMCP("Gemini Tool Server")
@mcp.tool()
def generate_reply(prompt: str) -> str:
    """プロンプトに対してVertex AIで応答を生成します。"""
    try:
        chat = chat_model.start_chat()
        resp = chat.send_message(prompt)
        return resp.text
    except Exception as e:
        print(f"Error calling Vertex AI: {e}")
        return "申し訳ありません、AIの応答生成でエラーが発生しました。"

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    print(f"Starting server on port {port}")
    asyncio.run(mcp.run_async(
        transport="streamable-http", host="0.0.0.0", port=port
    ))
