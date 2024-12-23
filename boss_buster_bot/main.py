from vector_db_initializer import build_vector_db_from_pdfs
from linebot_service import LineBotApp


def main():
    # 建立向量資料庫
    build_vector_db_from_pdfs(
        pdf_folder_path="./document",
        chunk_size=500,
        chunk_overlap=100,
        faiss_index_path="./faiss_index",
    )
    # 建立 LineBotApp 實例並執行
    app = LineBotApp()
    app.run()


if __name__ == "__main__":
    main()
