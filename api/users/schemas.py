import uuid
from typing import Optional, List

from pydantic import BaseModel


class UserToRoleSchema(BaseModel):
    # id: int
    # user: "UserReadSchema"
    role: "UserRoleSchema"

    class Config:
        from_attributes = True


class UserRoleSchema(BaseModel):
    id: int
    name: str
    description: str
    linked_permissions: List["UserRoleToPermissionSchema"]
    # users: List["UserReadSchema"]

    class Config:
        from_attributes = True


class UserRoleToPermissionSchema(BaseModel):
    permission: "UserRolePermissionSchema"

    # class Config:
    #     from_attributes = True


class UserRolePermissionSchema(BaseModel):
    id: int
    value: str
    description: str
    # role: UserRoleSchema
    # linked_roles: List["UserRoleSchema"]

    class Config:
        from_attributes = True


class UserRoleToPermissionSchema(BaseModel):
    id: int
    role: "UserRoleSchema"
    permission: "UserRolePermissionSchema"

    class Config:
        from_attributes = True


class UserReadSchema(BaseModel):
    id: int
    login: str
    name: str
    lastname: str
    # roles: List["UserToRoleSchema"]
    # comments_by: List[CommentsSchema]
    # messages: List[MessagesSchema]

    class Config:
        from_attributes = True
