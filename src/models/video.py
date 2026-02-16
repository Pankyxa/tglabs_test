import uuid
from datetime import datetime
from typing import List

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base


class Video(Base):
    __tablename__ = 'videos'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    creator_id: Mapped[uuid.UUID] = mapped_column(index=True)

    views_count: Mapped[int] = mapped_column(BigInteger, default=0)
    likes_count: Mapped[int] = mapped_column(BigInteger, default=0)
    comments_count: Mapped[int] = mapped_column(BigInteger, default=0)
    reports_count: Mapped[int] = mapped_column(BigInteger, default=0)

    video_created_at: Mapped[datetime]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]

    snapshots: Mapped[List["VideoSnapshot"]] = relationship(
        back_populates='video',
        cascade='all, delete-orphan',
    )


class VideoSnapshot(Base):
    __tablename__ = 'video_snapshots'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    video_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('videos.id'), index=True)

    views_count: Mapped[int] = mapped_column(BigInteger, default=0)
    likes_count: Mapped[int] = mapped_column(BigInteger, default=0)
    comments_count: Mapped[int] = mapped_column(BigInteger, default=0)
    reports_count: Mapped[int] = mapped_column(BigInteger, default=0)

    delta_views_count: Mapped[int] = mapped_column(BigInteger, default=0)
    delta_likes_count: Mapped[int] = mapped_column(BigInteger, default=0)
    delta_comments_count: Mapped[int] = mapped_column(BigInteger, default=0)
    delta_reports_count: Mapped[int] = mapped_column(BigInteger, default=0)

    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]

    video: Mapped[Video] = relationship(back_populates='snapshots')
