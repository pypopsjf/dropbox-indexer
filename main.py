"""main.py - Main entry point for the Dropbox file processing application."""
import os
import logging
from dotenv import load_dotenv

from dropbox_client import DropboxClient
from db import DropboxDB

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

load_dotenv()

DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")
DB_HOST=os.getenv("DB_HOST")
DB_PORT=os.getenv("DB_PORT")
DB_NAME=os.getenv("DB_NAME")
DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")

if not DROPBOX_ACCESS_TOKEN:
    raise ValueError("DROPBOX_ACCESS_TOKEN not found in .env file")
elif not DB_HOST:
    raise ValueError("DB_HOST not found in .env file")
elif not DB_PORT:
    raise ValueError("DB_PORT not found in .env file")
elif not DB_NAME:
    raise ValueError("DB_NAME not found in .env file")
elif not DB_USER:
    raise ValueError("DB_USER not found in .env file")
elif not DB_PASSWORD:
    raise ValueError("DB_PASSWORD not found in .env file")

# dropbox folder entry point (eg. "/path/to/index"). 
# Use "/" to get all folders and files in the root folder.

DROPBOX_STARTING_FOLDER = "/"


def main():
    """
    Main function to initialize the Dropbox client and database,
    and process the specified Dropbox folder.
    """
    logger = logging.getLogger(__name__)
    logger.info("Initializing Dropbox client...")
    db_client = DropboxDB(DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)

    logger.info("Initializing Dropbox database...")
    dropbox_client = DropboxClient(DROPBOX_ACCESS_TOKEN, db_client)

    logger.info("Getting folders and files from %s", DROPBOX_STARTING_FOLDER)
    processed = dropbox_client.process_dropbox_folder(DROPBOX_STARTING_FOLDER)

    logger.info(
        "Process complete. %d folders and %d files saved in database.",
        processed['nr_folders'],
        processed['nr_files']
    )

    db_client.close()


__version__ = "0.1.0"


if __name__ == "__main__":
    main()
