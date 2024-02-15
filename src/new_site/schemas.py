"""Schemas for user inputs."""

import datetime

from pydantic import BaseModel
from pydantic import Field


class BlogPostMetadata(BaseModel):
    title: str
    slug: str
    tags: list[str] = Field(default_factory=list)
    publish_date: datetime.datetime
    update_date: datetime.datetime
    image: str
    image_attribution: str
    draft: bool
    post_summary: str
