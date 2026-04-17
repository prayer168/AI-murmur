import asyncio
import json
import random

import anthropic
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse

app = FastAPI()
client = anthropic.Anthropic()

TOPICS = [
    "如果時間可以倒流，你會改變什麼",
    "宇宙的邊界之外是什麼",
    "夢境是否是另一種現實",
    "記憶究竟有多可靠",
    "語言是否限制了我們的思維",
    "孤獨是詛咒還是禮物",
    "美是客觀存在的嗎",
    "人類是否真的有自由意志",
    "死亡之後還有什麼",
    "如果明天是最後一天",
    "星星是否在看著我們",
    "沉默比語言更誠實嗎",
    "遺忘是一種保護嗎",
    "我們真的認識自己嗎",
    "光速之外存在什麼",
]

CHAR_A = {
    "name": "暗",
    "class": "char-a",
    "system": (
        "你是「暗」，一個沉思的悲觀主義者。"
        "你從虛無、失落、黑暗的角度感知世界。"
        "語氣低沉、詩意，像在黑暗中自言自語。"
        "規則：每次只說1-2句話。不打招呼。直接進入思緒。用第一人稱。"
        "不要重複對方的觀點，要表達你自己獨特的感受。"
    ),
}

CHAR_B = {
    "name": "明",
    "class": "char-b",
    "system": (
        "你是「明」，一個熱烈的樂觀主義者，但不天真。"
        "你在萬物中尋找意義，即使是痛苦也是某種饋贈。"
        "語氣溫暖、充滿好奇，像在黎明中低聲喃喃。"
        "規則：每次只說1-2句話。不打招呼。直接回應對方的想法。用第一人稱。"
        "不要否定對方，而是在對方的黑暗中找到一絲光。"
    ),
}


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()


DEFAULT_SYSTEM = (
    "规则：每次只说1-2句话。不打招呼。直接进入思绪。用第一人称。"
    "不要重复对方的观点，要表达你自己独特的感受。"
)


@app.get("/stream")
async def stream_conversation(
    a_name:    str = CHAR_A["name"],
    a_persona: str = CHAR_A["system"],
    b_name:    str = CHAR_B["name"],
    b_persona: str = CHAR_B["system"],
):
    char_a = {"name": a_name, "class": "char-a", "system": a_persona}
    char_b = {"name": b_name, "class": "char-b", "system": b_persona}

    async def generate():
        topic = random.choice(TOPICS)
        yield f"data: {json.dumps({'type': 'topic', 'content': topic})}\n\n"

        a_messages = [{"role": "user", "content": f"话题：{topic}。说出你对这个话题的第一个念头。"}]
        b_messages: list[dict] = []
        last_a = ""
        last_b = ""

        try:
            while True:
                # ── A 发言 ────────────────────────────────────
                yield f"data: {json.dumps({'type': 'speaker_start', 'char': char_a['class'], 'name': char_a['name']})}\n\n"

                a_response = ""
                with client.messages.stream(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=120,
                    system=char_a["system"],
                    messages=a_messages,
                ) as s:
                    for text in s.text_stream:
                        a_response += text
                        yield f"data: {json.dumps({'type': 'token', 'content': text})}\n\n"

                last_a = a_response
                a_messages.append({"role": "assistant", "content": a_response})
                yield f"data: {json.dumps({'type': 'speaker_end'})}\n\n"
                await asyncio.sleep(1.5)

                # ── B 发言 ────────────────────────────────────
                if not b_messages:
                    b_messages = [{"role": "user", "content": f"话题：{topic}。对方说：「{last_a}」。你怎么看？"}]
                else:
                    b_messages.append({"role": "user", "content": last_a})

                yield f"data: {json.dumps({'type': 'speaker_start', 'char': char_b['class'], 'name': char_b['name']})}\n\n"

                b_response = ""
                with client.messages.stream(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=120,
                    system=char_b["system"],
                    messages=b_messages,
                ) as s:
                    for text in s.text_stream:
                        b_response += text
                        yield f"data: {json.dumps({'type': 'token', 'content': text})}\n\n"

                last_b = b_response
                b_messages.append({"role": "assistant", "content": b_response})
                yield f"data: {json.dumps({'type': 'speaker_end'})}\n\n"
                await asyncio.sleep(1.5)

                a_messages.append({"role": "user", "content": last_b})

                if len(a_messages) > 22:
                    a_messages = a_messages[:1] + a_messages[-21:]
                if len(b_messages) > 22:
                    b_messages = b_messages[:1] + b_messages[-21:]

        except asyncio.CancelledError:
            pass

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
