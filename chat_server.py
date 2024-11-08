import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Header
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

# .envファイルから環境変数を読み込む
load_dotenv()

# APIキーを環境変数から取得
API_KEY = os.getenv("API_KEY")


# プロンプトテンプレートの作成
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "簡潔で正確な回答を提供してください:"),
        ("user", "{question}"),
    ],
)

# モデルの作成
model = ChatOllama(
    model="tinyllama",
    temperature=0,
)

# 出力パーサーの作成
parser = StrOutputParser()

# チェーンの作成
chain = prompt_template | model | parser

# FastAPIアプリケーションの初期化
app = FastAPI(title="Basic Chat API")


# チャットエンドポイントの定義
@app.get("/chat")
async def get_chat_response(question: str, api_key: str = Header(None)):
    # APIキーの検証
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    answer = chain.invoke({"question": question})
    return {"answer": answer}


# サーバーの起動
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9000)
