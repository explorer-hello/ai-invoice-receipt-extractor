import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'invoice_extractor'),
    'user': os.getenv('DB_USER', 'sunny'),
    'password': os.getenv('DB_PASSWORD', 'M.sunny@13')
}

# File upload settings
UPLOAD_DIR = "data/uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}