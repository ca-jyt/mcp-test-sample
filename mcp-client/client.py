import os
import asyncio
from fastmcp import Client
from fastapi import FastAPI, Request, BackgroundTasks
from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier

SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
MCP_URL = os.getenv("MCP_SERVER_URL")

slack = WebClient(token=SLACK_TOKEN)
verifier = SignatureVerifier(SLACK_SIGNING_SECRET)
app = FastAPI()

async def process_message_and_reply(text: str, channel: str):
    """AIへの問い合わせとSlackへの返信を行う非同期タスク"""
    async with Client(MCP_URL) as mcp:
        try:
            resp = await mcp.call_tool("generate_reply", {"prompt": text})
            reply = resp[0].text
        except Exception as e:
            print(f"Error calling MCP server: {e}")
            reply = "すみません、サーバーとの通信でエラーが発生しました。"
    slack.chat_postMessage(channel=channel, text=reply)

@app.post("/slack/events")
async def slack_events(req: Request, background_tasks: BackgroundTasks):
    body = await req.body()
    if not verifier.is_valid_request(body, req.headers):
        return {"error": "invalid signature"}
    data = await req.json()
    if "challenge" in data:
        return {"challenge": data["challenge"]}
    event = data.get("event", {})
    # "message" イベントの代わりに "app_mention" イベントを処理する
    if event.get("type") == "app_mention":
        # Slackからのテキストにはメンション(<@Uxxxxxxx>)が含まれているため、それを取り除く
        text = event["text"].split(">", 1)[-1].strip()
        channel = event["channel"]
        # AI処理をバックグラウンドタスクとして登録
        background_tasks.add_task(process_message_and_reply, text, channel)
        
    # SlackにはすぐにOKを返す
    return {"ok": True}
