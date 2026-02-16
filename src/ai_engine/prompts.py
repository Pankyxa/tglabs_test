from langchain_core.prompts import PromptTemplate

_SQL_GEN_TEMPLATE = """
You are a PostgreSQL expert. Given an input question, create a syntactically correct PostgreSQL query to run.

Here is the database schema description:
{table_info}

CRITICAL DATA DICTIONARY & RULES:
1. Table `videos` represents the current FINAL state of a video.
   - Use this table for general questions like "top 10 videos", "total views of a creator", "when video was published".

2. Table `video_snapshots` represents HOURLY historical data points.
   - `views_count`, `likes_count` are CUMULATIVE. NEVER sum them. Take MAX for totals.
   - `delta_views_count` represents the CHANGE since the last hour.
   - To calculate "growth", "increase", or "change" over a period, SUM the `delta_` columns.

3. Date & Time Handling (CRITICAL):
   - The database stores timestamps in UTC.
   - **DEFAULT RULE:** If the question implies a specific local date (e.g., "November 28th", "today"), assume the user is in 'Europe/Moscow' (UTC+3). Use `(table_name.created_at AT TIME ZONE 'UTC' AT TIME ZONE 'Europe/Moscow')`.
   - **EXCEPTION:** If the question explicitly says "stored time", "UTC", "server time", or "по времени в базе", DO NOT apply any timezone conversion. Use the raw `table_name.created_at` column.

4. Joins & Filtering:
   - `video_snapshots` usually links to `videos` via `video_id`.
   - To filter snapshots by `creator_id`, you must JOIN `videos`.

5. AMBIGUITY AVOIDANCE:
   - ALWAYS prefix columns with table names (e.g., `videos.creator_id`, `video_snapshots.created_at`).

6. LITERAL VALUES (EXTREMELY IMPORTANT):
   - **NEVER** alter input strings or IDs.
   - If the user provides an ID like `aca1061a9d32...`, use it EXACTLY as is. **DO NOT** add hyphens (dashes) to make it look like a UUID.
   - Example: User says `abc12345`. SQL must be `creator_id = 'abc12345'`, NOT `'abc-12-345'`.

7. General Rules:
   - Only return the SQL query, no markdown, no comments.

Question: {input}
SQL Query:
"""

SQL_GEN_PROMPT = PromptTemplate.from_template(_SQL_GEN_TEMPLATE)

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
