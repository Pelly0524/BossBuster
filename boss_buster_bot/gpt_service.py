from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from openai import OpenAI
import os
import re

# 初始化 OpenAI API 用戶端
client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

# 載入已經建立好的向量資料庫
vector_db = FAISS.load_local(
    "./faiss_index", OpenAIEmbeddings(), allow_dangerous_deserialization=True
)


def get_law_based_answer(user_input: str) -> str:
    """
    給定使用者輸入(可能是故事情境或問法條問題)，
    從向量資料庫查詢最相關段落，然後丟給 GPT 產生回答。
    最後在回答中顯示出處。
    """

    # 1. 在向量資料庫做相似度搜尋，找出 k 個最相近的段落
    docs = vector_db.similarity_search(user_input, k=4)

    # 2. 組合 context，包含來源 metadata
    #    這裡把「chunk 內容」和「來源資料」一起合成
    context_segments = []
    for doc in docs:
        source_info = doc.metadata.get("source", "未知來源")
        # 你也可以加上頁數、chunk_id 等額外資訊
        chunk_text = doc.page_content
        segment_text = f"[來源: {source_info}]\n{chunk_text}"
        context_segments.append(segment_text)

    context_text = "\n\n".join(context_segments)

    # 3. 建立 prompt，告訴 GPT 要在回答中參考以下段落，必要時可引用[來源]
    #    也可以在回答完後加個「參考來源」小結
    prompt = f"""你是一位熟悉勞基法的諮詢顧問。以下是與問題相關的段落及其來源：
    {context_text}

    請根據以上內容，使用繁體中文回答使用者的問題。問題如下：
    {user_input}
    """

    try:
        completion = client.chat.completions.create(
            model="o1-preview",
            messages=[
                {"role": "user", "content": prompt},
            ],
        )
        answer = completion.choices[0].message.content.strip()
        return remove_markdown_bold(answer)
    except Exception as e:
        return f"發生錯誤：{str(e)}"


def remove_markdown_bold(text: str) -> str:
    return re.sub(r"\*\*(.*?)\*\*", r"\1", text)


if __name__ == "__main__":
    user_input = "如果我在週六的晚上臨時被叫去加班，法律上有什麼規定？"
    answer = get_law_based_answer(user_input)
    print(answer)
