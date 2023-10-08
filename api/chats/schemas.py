from api.communication.schemas import ChatUser, UserSourceSchema


class ChatUserWithUnseen(ChatUser):
    unseen: int


class ChatUserWithUserSourceSchema(ChatUser):
    user_source: UserSourceSchema
