# 打擊慣老闆！

這是一個結合 **Line Bot** 和 **RAG**（檢索增強生成）的工具，幫助使用者快速查詢台灣勞基法，分析各種職場情境，保護你的合法權益。

---

## 📌 專案特色

- **勞基法查詢**：  
  輸入自然語言，即可快速查詢勞基法相關條文。

- **情境分析**：  
  針對輸入的職場問題，提供相關法規建議。

- **即時互動**：  
  基於 Line Bot 平台，隨時隨地為你解答。

---

## 🛠 技術架構

- **Line Bot SDK**：與 LINE 平台進行互動。
- **RAG**（Retrieval-Augmented Generation）：結合搜尋與生成模型。
- **OpenAI GPT**：實現智能問答功能。
- **Flask**：輕量級後端框架。

---

## ⚙️ 環境需求

- **Python**：版本 3.9.13。
- **LINE 開發者帳號**：用於設置 LINE Bot。
- **OpenAI API 金鑰**：用於 GPT 問答功能。

---

## 🚀 安裝步驟

1. **克隆專案**：

    ```bash
    git clone https://github.com/Pelly0524/BossBuster.git
    cd boss_buster_bot
    ```

2. **建立虛擬環境並安裝依賴**：

    ```bash
    python -m venv venv
    source venv/bin/activate  # 或 .\\venv\\Scripts\\activate（Windows）
    pip install -r requirements.txt
    ```

3. **設定環境變數**：

    新增 `.env` 文件，並填入以下內容：

    ```env
    LINE_CHANNEL_ACCESS_TOKEN=你的_LINE_Channel_Access_Token
    LINE_CHANNEL_SECRET=你的_LINE_Channel_Secret
    OPENAI_API_KEY=你的_OpenAI_API_Key
    ```

4. **啟動伺服器**：

    ```bash
    python main.py
    ```

5. **使用 ngrok 將伺服器公開**：

    ```bash
    ngrok http 5000
    ```

    將 ngrok 提供的網址設定為 LINE Webhook URL。

---

## 📖 使用說明

1. **將 Line Bot 加入好友**。
2. **輸入職場問題或關鍵字**。
3. **接收法規建議與情境分析**。

---

## 👨‍💻 開發者資訊

- **開發者**：Pelly  
- **聯絡方式**：pelly1234@gmail.com  
- **GitHub**：https://github.com/Pelly0524

---

## ⚠️ 授權條款

本專案保留所有權利，未經許可，不得用於任何商業用途。

---

## 📝 未來規劃

- 增加更多法規範疇支持。
- 提供多語言支持。
- 優化情境分析模型。

---
