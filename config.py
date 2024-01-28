import os

from dotenv import load_dotenv

load_dotenv()


YOUR_DB = os.environ.get("YOUR_DB")
YOUR_USER = os.environ.get("YOUR_USER")
YOUR_PASSWORD = os.environ.get("YOUR_PASSWORD")
YOUR_HOST = os.environ.get("YOUR_HOST")
YOUR_PORT = os.environ.get("YOUR_PORT")

DATABASE_URL = f"postgresql://{YOUR_USER}:{YOUR_PASSWORD}@{YOUR_HOST}:{YOUR_PORT}/{YOUR_DB}"