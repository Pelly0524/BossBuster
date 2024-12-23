from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import os
import glob
import PyPDF2
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def build_vector_db_from_pdfs(
    pdf_folder_path: str = "./document",
    chunk_size: int = 500,
    chunk_overlap: int = 100,
    faiss_index_path: str = "./faiss_index",
):
    """
    從指定的 pdf_folder_path 中，讀取所有 PDF 檔，分塊後做向量化，並存入 FAISS Index。

    :param pdf_folder_path: PDF 檔案所在資料夾
    :param chunk_size: 每個分塊的最大字數
    :param chunk_overlap: 分塊之間的重疊字數，讓上下文連貫
    :param faiss_index_path: FAISS 向量庫儲存檔案路徑
    """

    # 準備一個裝所有 (文本, metadata) 的 list
    all_docs = []

    # 取得所有 PDF 檔案路徑
    pdf_files = glob.glob(os.path.join(pdf_folder_path, "*.pdf"))

    for pdf_file in pdf_files:
        # 讀取 PDF 的全文
        text = extract_text_from_pdf(pdf_file)

        # 做文字分塊
        text_chunks = chunk_text(text, chunk_size, chunk_overlap)

        # 把每一塊文字與它對應的 metadata(來源檔名、chunk編號)一起存起來
        for i, chunk in enumerate(text_chunks):
            metadata = {
                "source": os.path.splitext(os.path.basename(pdf_file))[
                    0
                ],  # 來源 PDF 檔名
                "chunk_index": i,  # 可以記錄 chunk 順序
            }
            all_docs.append((chunk, metadata))

    if not all_docs:
        print("沒有找到任何 PDF 文字內容，請確認 PDF 路徑或檔案內容。")
        return

    # 準備 Embedding 模型
    embeddings = OpenAIEmbeddings()  # 使用 OpenAI Embeddings（需 API Key）

    # 利用 from_texts_and_metadatas 建立向量索引，並把所有 metadata 帶入
    print("建立向量索引 (FAISS)...")
    vector_store = FAISS.from_texts(
        texts=[doc[0] for doc in all_docs],  # 文字內容
        embedding=embeddings,  # Embedding 模型
        metadatas=[doc[1] for doc in all_docs],  # 每段文字對應的 metadata
    )

    # 將建立好的向量資料庫儲存到本地檔案
    print(f"儲存 FAISS 索引到 {faiss_index_path}")
    vector_store.save_local(faiss_index_path)
    print("完成向量資料庫建立！")


def extract_text_from_pdf(pdf_file_path: str) -> str:
    """
    簡單使用 PyPDF2 抽取 PDF 文字。
    如果遇到無法抽取或加密的 PDF，可能要改用 pdfminer.six。
    """
    text_content = []
    with open(pdf_file_path, "rb") as f:
        pdf_reader = PyPDF2.PdfReader(f)
        for page in pdf_reader.pages:
            text_content.append(page.extract_text() or "")
    return "\n".join(text_content)


def chunk_text(text: str, chunk_size: int, chunk_overlap: int) -> list:
    """
    使用 langchain 提供的 RecursiveCharacterTextSplitter 進行文字分塊。
    會回傳一個 list，每個元素都是一段分塊後的文字。
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)


if __name__ == "__main__":
    build_vector_db_from_pdfs(
        pdf_folder_path="./document",
        chunk_size=500,
        chunk_overlap=100,
        faiss_index_path="./faiss_index",
    )
