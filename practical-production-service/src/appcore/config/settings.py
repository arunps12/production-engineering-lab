import os

def get_settings():
    return {
        "app_name": os.getenv("APP_NAME", "appcore"),
        "debug": os.getenv("DEBUG", "false").lower() == "true",
        "port": int(os.getenv("PORT", "8000")),
    }