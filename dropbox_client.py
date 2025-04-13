"""
This module provides a client for interacting with Dropbox API.
"""
import logging
import dropbox
from dropbox.exceptions import DropboxException

logger = logging.getLogger(__name__) 


class DropboxClient:
    """
    A client for interacting with Dropbox API.
    This class handles authentication and provides a methods to list folders 
    and files recursively, and save the metadata to a database.
    It requires an access token for authentication and a db.DropboxDB instance.
    """

    def __init__(self, access_token=None, dropbox_db=None):
        if access_token is None:
            raise ValueError("Access token is required")
        try:
            self.dbx = dropbox.Dropbox(access_token)
        except DropboxException as e:
            raise DropboxException(f"API call failed: {e}") from e
        
        if dropbox_db is None:
            raise ValueError("Dropbox database is required")
        self.dropbox_db = dropbox_db

    def process_dropbox_folder(self, folder_path):
        """
        Process a Dropbox folder and its contents recursively.
        This method lists all folders and files in the specified folder path,
        and saves their metadata to the database.
        It returns a dictionary with the number of folders and files processed.
        """
        processed = dict()
        processed['nr_folders'] = 0
        processed['nr_files'] = 0

        try:
            result = self.dbx.files_list_folder(folder_path, recursive=True)
 
            while True:
                for entry in result.entries:
                    if isinstance(entry, dropbox.files.FolderMetadata):
                        # Process folder
                        self.dropbox_db.upsert_dropbox_folder(entry)
                        logger.info("Folder %s saved in dropbox_folders.", entry.path_display)
                        processed['nr_folders'] += 1
                    elif isinstance(entry, dropbox.files.FileMetadata):
                        # Process file
                        self.dropbox_db.upsert_dropbox_file(entry)
                        logger.info("File %s saved in dropbox_files.", entry.path_display)
                        processed['nr_files'] += 1

                # Check if there are more entries to fetch
                if not result.has_more:
                    break
                result = self.dbx.files_list_folder_continue(result.cursor)
                
        except DropboxException as e:
            raise DropboxException(f"API call failed: {e}") from e
        
        finally:
            self.dbx.close()
        
        return processed
