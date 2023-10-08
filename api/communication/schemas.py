from typing import Optional

from fastapi import Query
from pydantic import BaseModel, Field

from api.communication.models import AttachmentTypes
from api.users.schemas import UserReadSchema


class ChatUser(BaseModel):
    id: int
    name: str
    user_source_id: int
    platform_id: Optional[int]
    platform_login: Optional[str]
    banned: Optional[bool]

    class Config:
        orm_mode = True


class UserSourceSchema(BaseModel):
    id: int
    title: str
    icon_url: str
    enabled: bool


class MessageSchema(BaseModel):
    id: int
    user: Optional[ChatUser]
    reply_user: Optional[UserReadSchema]

    is_reply: Optional[bool]
    chat_id: int

    text: Optional[str]
    attachment: Optional[str]
    attachment_type: Optional[AttachmentTypes]
    message_seen: Optional[bool] = Field(default=True)

    class Config:
        orm_mode = True


class MessageCreate(BaseModel):
    user_id: Optional[int] = Field(default=None)
    reply_user_id: Optional[int] = Field(default=None)

    is_reply: Optional[bool] = Field(default=False)
    chat_id: int = Field(default=None)

    text: Optional[str] = Field(default=None)
    attachment: Optional[str] = Field(default=None)
    attachment_type: Optional[AttachmentTypes] = Field(default=AttachmentTypes.no_attachment)


class GetByUserId(BaseModel):
    user_id: int = Field(Query(title='User Id'))
