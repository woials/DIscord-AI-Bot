import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel,Field,TypeAdapter
from typing import List,Literal

class Paragraph(BaseModel):
    type:Literal["paragraph"]="paragraph"
    text:str

class Headline(BaseModel):
    type:Literal["headline"]="headline"
    text:str

Block=Paragraph | Headline

class GeminiArticle(BaseModel):
    title:str=Field(description="タイトル")
    summary:str=Field(description="内容の要約")
    main_text:List[Block]=Field(description="本文を構成するブロックのリスト。見出し(headline)と段落(paragraph)を適切な順番で並べてください")

load_dotenv()
client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

async def get_gemini_result(query: str) -> GeminiArticle:
    model = "gemini-3.1-flash-lite"  # ✅ これは正しかった
    response = await client.aio.models.generate_content(  # ✅ clientから呼ぶ
        model=model,
        contents=query,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=GeminiArticle
        )
    )
    result=response.parsed #response.parsedの戻り値はBaseModel | dict | Enum | Noneと定義されていてGeminiArticleで返って来ると動的な推論ができない
    assert isinstance(result,GeminiArticle) #resultがGeminiArticle型かどうかをチェック
    return result
