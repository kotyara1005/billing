import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:dbpass@pg:5432/db")
