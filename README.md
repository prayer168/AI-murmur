# AI · 喃喃

兩個 AI 角色在書香古風的畫面裡無限喃喃自語，你是那個靜靜窺聽的旁觀者。

**示範版（無需 API Key）** → [prayer168.github.io/AI-murmur](https://prayer168.github.io/AI-murmur/)

---

## 畫面預覽

| 功能 | 說明 |
|------|------|
| 宣紙背景 | SVG 噪點纖維紋理 + 竹簡橫紋 + 墨染暗角 |
| 竹子裝飾 | 左下角三杆水墨竹，右上角朱砂印章 |
| 深度層次 | 新訊息清晰，舊訊息逐層模糊退遠 |
| 打字動畫 | 思考三點 → 逐字浮現 → 標點後自然停頓 |

---

## 主要功能

- **兩個 AI 角色無限對話** — 「暗」（悲觀）與「明」（樂觀）圍繞隨機話題喃喃不停
- **暫停 ⏸ / 停止 ■** — 空白鍵或按鈕，隨時凍結或終止對話
- **換個話題** — 存檔當前對話，立即開始新一輪
- **角色設定 ⚙** — 自訂名字、頭像 emoji、性格描述，6 種預設快選
- **話題歷史 ☰** — 自動存檔每輪對話，點擊展開回顧
- **移動端適配** — 手機、平板皆可使用

---

## 本地啟動

### 環境需求

- Python 3.9+
- [Anthropic API Key](https://console.anthropic.com)

### 步驟

```bash
# 1. 克隆專案
git clone https://github.com/prayer168/AI-murmur.git
cd AI-murmur

# 2. 安裝依賴
pip install -r requirements.txt

# 3. 設定 API Key
# Windows CMD
set ANTHROPIC_API_KEY=sk-ant-xxxxxxxx
# macOS / Linux
export ANTHROPIC_API_KEY=sk-ant-xxxxxxxx

# 4. 啟動伺服器
uvicorn app:app --reload

# 5. 開啟瀏覽器
# http://localhost:8000
```

---

## 雲端部署

### Railway（推薦，支援完整 AI 功能）

1. 前往 [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub repo**
2. 選擇 `AI-murmur`
3. 在 **Variables** 加入：`ANTHROPIC_API_KEY = sk-ant-xxxxxxxx`
4. 部署完成後取得公開網址

### GitHub Pages（靜態示範模式）

已自動啟用，網址：[prayer168.github.io/AI-murmur](https://prayer168.github.io/AI-murmur/)

> 靜態版不需要 API Key，會自動播放內建示範對話。

---

## 技術架構

```
前端 (index.html)          後端 (app.py)
─────────────────          ──────────────
純 HTML / CSS / JS    ←→   FastAPI + Server-Sent Events
EventSource 串流           Anthropic Claude Haiku
書香古風 UI                兩個角色獨立對話歷史
深度層次動畫               無限話題輪轉
```

**使用模型**：`claude-haiku-4-5-20251001`（速度快、成本低，適合即時串流）

---

## 授權

MIT License
