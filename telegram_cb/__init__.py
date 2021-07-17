from .listeners import main
from .settings import API_HASH, API_ID, BASE_DIR

if __name__ == "__main__":
    base_dir = BASE_DIR
    main("session_name", API_ID, API_HASH, "@handle")
