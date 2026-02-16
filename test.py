import asyncio
from src.ai_engine.assistant import SQLAssistant


async def main():
    assistant = SQLAssistant()
    print("Assistant created.")

    question = "Сколько видео всего?"
    print(f"Asking: {question}")

    answer = await assistant.ask(question)

    print(f"Answer: {answer}")


if __name__ == '__main__':
    asyncio.run(main())