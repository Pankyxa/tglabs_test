import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel


class SnapshotSchema(BaseModel):
    id: uuid.UUID
    video_id: uuid.UUID

    views_count: int
    likes_count: int
    comments_count: int
    reports_count: int

    delta_views_count: int
    delta_likes_count: int
    delta_comments_count: int
    delta_reports_count: int

    created_at: datetime
    updated_at: datetime


class VideoSchema(BaseModel):
    id: uuid.UUID
    creator_id: uuid.UUID

    views_count: int
    likes_count: int
    comments_count: int
    reports_count: int

    video_created_at: datetime
    created_at: datetime
    updated_at: datetime

    snapshots: List[SnapshotSchema]


class RootSchema(BaseModel):
    videos: List[VideoSchema]
