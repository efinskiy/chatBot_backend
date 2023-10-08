from sqlalchemy import ForeignKey, String, MetaData
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import List
from api.models import Base


metadata = MetaData()


class User(Base):
    __tablename__ = 'User'
    metadata = metadata

    login: Mapped[str] = mapped_column(String(30))
    name: Mapped[str] = mapped_column(String(36))
    lastname: Mapped[str] = mapped_column(String(36))
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)

    roles: Mapped[List['UserToRole']] = relationship(back_populates='user')
    comments_by: Mapped[List['UserCommentary']] = relationship(back_populates='created_by')
    messages: Mapped[List['Message']] = relationship(back_populates='reply_user')


class UserToRole(Base):
    __tablename__ = 'UserToRole'
    metadata = metadata

    user: Mapped["User"] = relationship(back_populates='roles')
    user_id: Mapped[int] = mapped_column(ForeignKey('User.id'))

    role: Mapped['UserRole'] = relationship(back_populates='users')
    role_id: Mapped[int] = mapped_column(ForeignKey('UserRole.id'))


class UserRole(Base):
    __tablename__ = 'UserRole'
    metadata = metadata

    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(128))
    users: Mapped[List['UserToRole']] = relationship(back_populates='role')
    linked_permissions: Mapped[List['UserRoleToPermission']] = relationship(back_populates='role')


class UserRolePermission(Base):
    __tablename__ = 'UserRolePermission'
    metadata = metadata

    value: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(String(128))
    linked_roles: Mapped[List["UserRoleToPermission"]] = relationship(
        back_populates="permission", cascade="all, delete-orphan"
    )


class UserRoleToPermission(Base):
    __tablename__ = 'UserRoleToPermission'
    metadata = metadata

    role_id: Mapped[int] = mapped_column(ForeignKey("UserRole.id"))
    permission_id: Mapped[int] = mapped_column(ForeignKey("UserRolePermission.id"))

    role: Mapped["UserRole"] = relationship(back_populates='linked_permissions')
    permission: Mapped["UserRolePermission"] = relationship(back_populates='linked_roles')
