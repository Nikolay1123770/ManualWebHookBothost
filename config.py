import os
from dataclasses import dataclass

@dataclass
class Config:
    TELEGRAM_TOKEN: str = os.environ.get("TELEGRAM_TOKEN", "")
    WEBHOOK_URL: str = os.environ.get("WEBHOOK_URL", "")
    PORT: int = int(os.environ.get("PORT", 5000))
    DEBUG: bool = os.environ.get("DEBUG", "false").lower() == "true"
    
    BOT_USERNAME: str = ""
    ADMIN_IDS: list = None
    
    def __post_init__(self):
        if self.ADMIN_IDS is None:
            self.ADMIN_IDS = []

config = Config()
