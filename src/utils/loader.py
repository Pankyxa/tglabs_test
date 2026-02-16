import asyncio
import json
from pathlib import Path

from src.db import async_session_factory, engine, Base
from src.models.video import Video, VideoSnapshot
from src.schemas.videos import RootSchema

DATA_FILE = Path(__file__).parent.parent.parent / 'videos.json'


async def load_data():
    print(f'Ищем файл: {DATA_FILE}')

    if not (DATA_FILE.exists()):
        print('Файл videos.json не найден! Загрузи его в корень проекта.')
        return

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    try:
        parsed_data = RootSchema(**raw_data)
        print(f'Pydantic: Данные валидны. Видео: {len(parsed_data.videos)}')
    except Exception as e:
        print(f'Ошибка в структуре json: {e}')
        return

    print('Пересоздаем структуру БД')
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    print('Начинаем запись в БД')
    async with async_session_factory() as session:
        videos_to_add = []

        for video_schema in parsed_data.videos:
            video_data = video_schema.model_dump(exclude={'snapshots'})

            for key, value in video_data.items():
                if hasattr(value, 'replace') and value.tzinfo is not None:
                    video_data[key] = value.replace(tzinfo=None)

            video_orm = Video(**video_data)

            for snap_schema in video_schema.snapshots:
                snap_data = snap_schema.model_dump(exclude={'video_id'})

                for key, value in snap_data.items():
                    if hasattr(value, 'replace') and value.tzinfo is not None:
                        snap_data[key] = value.replace(tzinfo=None)

                snapshot_orm = VideoSnapshot(**snap_data)

                video_orm.snapshots.append(snapshot_orm)

            videos_to_add.append(video_orm)

        session.add_all(videos_to_add)
        await session.commit()
        print(f'Успешно загружено: {len(videos_to_add)} видео и их снапшоты')


if __name__ == '__main__':
    asyncio.run(load_data())
