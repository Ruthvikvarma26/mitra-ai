from datetime import datetime, timedelta, UTC

from jose import jwt

from backend.app.core.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)


def create_access_token(data: dict):
    # Copy the data so we don't modify the original dictionary
    to_encode = data.copy()

    # Set the expiry time
    expire = datetime.now(UTC) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # Add expiry to the payload
    to_encode.update({"exp": expire})

    # Create and sign the JWT
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt