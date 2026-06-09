import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

#Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Gideon@localhost/epl_matches")
API_TOKEN = os.getenv("API_TOKEN","12c0151a71964fcdb24ada0e2381e5fc")