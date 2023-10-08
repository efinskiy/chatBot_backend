from fastapi import APIRouter
from .users.routes import router as users_router
from .auth.routes import router as auth_router
from .communication.routes import router as comm_router
from .chats.routes import router as chat_router


router = APIRouter(prefix='/api')

router.include_router(users_router)
router.include_router(comm_router)
router.include_router(auth_router)
router.include_router(chat_router)
