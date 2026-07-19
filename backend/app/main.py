from fastapi import FastAPI
from backend.app.db.database import Base,engine
from backend.app.models.user import User
from backend.app.core.security import hash_password, verify_password
from backend.app.api.routes.auth import router as auth_router
from backend.app.core.jwt import create_access_token
from fastapi import Depends
from backend.app.core.auth import get_current_user
from backend.app.core.auth import require_admin
from backend.app.api.routes.personality import router as personality_router
from backend.app.models.chat_session import ChatSession
from backend.app.models.message import Message
from backend.app.api.routes.chat import router as chat_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(personality_router)
app.include_router(chat_router)
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to Mitra Backend 🚀"}


@app.get("/health")
def health_check():
    try:
        connection = engine.connect()
        connection.close()

        return {
            "status": "healthy",
            "database": "Connected ✅"
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }
@app.get("/test-hash")
def test_hash():

    password = "hello123"

    hashed = hash_password(password)

    verified = verify_password(password, hashed)

    return {
        "original_password": password,
        "hashed_password": hashed,
        "verified": verified
    }

@app.get("/test-token")
def test_token():
    token = create_access_token(
        data={"sub": "ruthvik@gmail.com"}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
@app.get("/profile")
def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
    }

@app.get("/admin")
def admin_dashboard(
    current_user: User = Depends(require_admin)
):
    return {
        "message": "Welcome Admin!",
        "admin": current_user.name
    }