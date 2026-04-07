import os
from typing import List, Dict

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class Generator:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)

    def build_context(self, results: List[Dict]) -> str:
        parts = []
        for i, result in enumerate(results, start=1):
            doc = result["document"]
            parts.append(f"[文書{i}]\n{doc['text']}")
        return "\n\n".join(parts)

    def answer(self, query: str, results: List[Dict]) -> str:
        context = self.build_context(results)

        prompt = f"""あなたはRAGのQAアシスタントです。
与えられた参照文書だけを根拠にして、質問に答えてください。
参照文書に答えがない場合は「参照文書からは分かりません」と答えてください。

参照文書:
{context}

質問:
{query}

回答:"""

        response = self.client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
        )

        return response.output_text