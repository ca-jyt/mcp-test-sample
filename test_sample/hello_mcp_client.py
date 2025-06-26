import asyncio
from fastmcp.client import Client

async def main():
    # FastMCPサーバーの正しいエンドポイントを指定します。
    # 一般的に、fastmcpは /v1 というプレフィックスを使用します。
    # Clientオブジェクト自体にはベースURLを指定し、
    # call_toolが内部で正しいパスを組み立てます。
    # URLの末尾にスラッシュは不要です。
    async with Client("http://127.0.0.1:8000/v1/") as client:
        result = await client.call_tool("hello", {"name": "クラウドエース"})
        print("結果:", result)

if __name__ == "__main__":
    asyncio.run(main())
