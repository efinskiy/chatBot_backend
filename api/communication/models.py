from typing import Optional, List

from sqlalchemy import DateTime, func, String, ForeignKey, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from api.models import Base
import enum
from ..users.models import User

from sqlalchemy import MetaData

metadata = MetaData()


class AttachmentTypes(enum.Enum):
    image = 0
    voice = 1
    geo = 2
    file = 3
    no_attachment = 4


class UserSource(Base):
    __tablename__ = 'UserSource'
    metadata = metadata

    title: Mapped[str] = mapped_column(String(32))
    icon_url: Mapped[str] = mapped_column(String(512))
    enabled: Mapped[Optional[bool]] = mapped_column(default=False)

    users: Mapped[List["ChatUser"]] = relationship(back_populates='user_source')


class UserCommentary(Base):
    __tablename__ = 'UserCommentary'
    metadata = metadata

    user_id: Mapped[int] = mapped_column(ForeignKey('ChatUser.id'))
    user: Mapped["ChatUser"] = relationship(back_populates='comments')
    message: Mapped[str] = mapped_column(String(512))
    created_by: Mapped["User"] = relationship(back_populates='comments_by')
    created_by_id: Mapped[int] = mapped_column(ForeignKey(User.id))


class ChatUser(Base):
    __tablename__ = 'ChatUser'
    metadata = metadata

    name: Mapped[str]
    user_source_id: Mapped[int] = mapped_column(ForeignKey("UserSource.id"))
    platform_id: Mapped[Optional[int]]
    platform_login: Mapped[Optional[str]]
    chat_id: Mapped[Optional[int]]
    banned: Mapped[Optional[bool]] = mapped_column(default=False)
    user_source: Mapped["UserSource"] = relationship(back_populates='users')
    comments: Mapped[List["UserCommentary"]] = relationship(back_populates='user')
    messages: Mapped[List["Message"]] = relationship(back_populates='user')


class Message(Base):
    __tablename__ = 'Message'
    metadata = metadata

    user: Mapped[Optional["ChatUser"]] = relationship(back_populates='messages')
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey('ChatUser.id'))

    reply_user: Mapped[Optional["User"]] = relationship(back_populates='messages')
    reply_user_id: Mapped[Optional[int]] = mapped_column(ForeignKey(User.id))

    is_reply: Mapped[Optional[bool]] = mapped_column(default=False)
    chat_id: Mapped[int]

    text: Mapped[Optional[str]]
    attachment: Mapped[Optional[str]]
    attachment_type: Mapped[Optional[AttachmentTypes]] = mapped_column(Enum(AttachmentTypes),
                                                                       default=AttachmentTypes.no_attachment)

    message_seen: Mapped[Optional[bool]] = mapped_column(default=False)


