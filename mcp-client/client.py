import os
import asyncio
from fastmcp import Client
from fastapi import FastAPI, Request
from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier
SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
MCP_URL = os.getenv("MCP_SERVER_URL")
slack = WebClient(token=SLACK_TOKEN)
verifier = SignatureVerifier(SLACK_SIGNING_SECRET)
app = FastAPI()
@app.post("/slack/events")
async def slack_events(req: Request):
    body = await req.body()
    if not verifier.is_valid_request(body, req.headers):
        return {"error": "invalid signature"}
    data = await req.json()
    if "challenge" in data:
        return {"challenge": data["challenge"]}
    event = data.get("event", {})
    if event.get("type") == "message" and "bot_id" not in event:
        text = event["text"]
        channel = event["channel"]
        async with Client(MCP_URL) as mcp:
            resp = await mcp.call_tool("generate_reply", {"prompt": text})
            reply = resp[0].text
        slack.chat_postMessage(channel=channel, text=reply)
    return {"ok": True}
