from fastmcp.server.server import FastMCP, create_streamable_http_app
from fastmcp.tools.tool import FunctionTool
import uvicorn

# ツール定義
async def hello(name: str) -> str:
    return f"Hello, {name}!"

hello_tool = FunctionTool(
    name="hello",
    description="Say hello to someone",
    parameters={
        "name": {
            "type": "string",
            "description": "The name of the person to greet"
        }
    },
    fn=hello,
)

# FastMCP インスタンス生成
fastmcp = FastMCP(
    name="HelloMCP",
    instructions="This MCP greets users.",
    tools=[hello_tool],
)

# --- ここからが修正部分です ---

# ASGIアプリを構築する際に、必須引数としてエンドポイントのパスを指定します
# 一般的なRESTful APIの慣例に従い、'/v1' を指定します
app = create_streamable_http_app(fastmcp, "/v1")

# --- ここまでが修正部分です ---


# Uvicorn で起動
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
