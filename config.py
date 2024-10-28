import os
import secrets
secret_key = secrets.token_hex(16)

class Config:
    SECRET_KEY = secret_key
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit

config = Config()