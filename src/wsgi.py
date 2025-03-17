import os

from src.app import create_app

app = create_app(environment=os.getenv("ENVIRONMENT"))
