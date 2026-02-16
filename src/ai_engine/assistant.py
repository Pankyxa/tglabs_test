from sqlalchemy import text
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from src.settings import settings
from src.ai_engine.prompts import SQL_GEN_PROMPT, ANSWER_PROMPT
from src.ai_engine.db_helper import get_async_engine, get_schema_info


class SQLAssistant:
    def __init__(self):
        self.engine = get_async_engine()
        self.table_info = get_schema_info()

        self.llm = ChatOpenAI(
            model=settings.openrouter_model,
            api_key=settings.openrouter_api_key,
            base_url="https://openrouter.ai/api/v1",
            temperature=0,
            max_tokens=1000
        )

        self._build_chains()

    def _build_chains(self):
        """Собирает пайплайны обработки LangChain."""
        self.sql_gen_chain = (
                RunnablePassthrough.assign(table_info=lambda x: self.table_info)
                | SQL_GEN_PROMPT
                | self.llm
                | StrOutputParser()
        )

        self.answer_chain = (
                ANSWER_PROMPT
                | self.llm
                | StrOutputParser()
        )

    async def ask(self, question: str) -> str:
        try:
            generated_sql = await self.sql_gen_chain.ainvoke({"input": question})
            clean_sql = self._clean_sql(generated_sql)

            result_data = await self._execute_sql(clean_sql)

            final_answer = await self.answer_chain.ainvoke({
                "question": question,
                "query": clean_sql,
                "result": str(result_data)
            })

            return self._clean_answer(final_answer)

        except Exception as e:
            print(f"Async SQL Assistant Error: {e}")
            return "0"

    async def _execute_sql(self, sql: str) -> list:
        """Выполняет сырой SQL через SQLAlchemy AsyncEngine."""
        async with self.engine.connect() as conn:
            result = await conn.execute(text(sql))
            return result.fetchall()

    @staticmethod
    def _clean_sql(sql_text: str) -> str:
        return sql_text.replace("```sql", "").replace("```", "").strip()

    @staticmethod
    def _clean_answer(answer_text: str) -> str:
        clean = answer_text.strip()
        if clean.endswith('.') and clean[:-1].isdigit():
            clean = clean[:-1]
        return clean