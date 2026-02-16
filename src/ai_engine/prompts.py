from langchain_core.prompts import PromptTemplate

# Промпт для генерации SQL
_SQL_GEN_TEMPLATE = """
You are a PostgreSQL expert. Given an input question, create a syntactically correct PostgreSQL query to run.

Here is the database schema description:
{table_info}

CRITICAL DATA DICTIONARY & RULES:
1. Table `videos` represents the current FINAL state of a video.
   - Use this table for general questions like "top 10 videos", "total views of a creator".

2. Table `video_snapshots` represents HOURLY historical data points.
   - `views_count`, `likes_count`, etc. in this table are CUMULATIVE (running totals).
   - NEVER sum `views_count` in `video_snapshots`. To get the total, take the MAX value.
   - `delta_views_count`, `delta_likes_count` represent the CHANGE (increase) since the last hour.
   - If asked about "activity during a specific period" (e.g., "how many views yesterday"), SUM the `delta_` columns.
   - Filter by `created_at` correctly.

3. General Rules:
   - Unless otherwise specified, do not return more than 5 rows.
   - Only return the SQL query, no markdown, no comments.

Question: {input}
SQL Query:
"""

SQL_GEN_PROMPT = PromptTemplate.from_template(_SQL_GEN_TEMPLATE)

# Промпт для интерпретации ответа в число
_ANSWER_TEMPLATE = """Given the SQL result, extract the numerical answer.

Question: {question}
SQL Query: {query}
SQL Result: {result}

CRITICAL INSTRUCTIONS:
- Return ONLY the raw number (integer or float).
- Do NOT write words like "Answer:", "Result:", "views", etc.
- If the SQL Result is a list like `[(14639,)]`, return `14639`.
- If the SQL Result is empty `[]`, return `0`.
- Do not use markdown formatting.

Final Number:"""

ANSWER_PROMPT = PromptTemplate.from_template(_ANSWER_TEMPLATE)