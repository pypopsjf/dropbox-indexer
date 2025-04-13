"""db.py - Database connection and statements for saving Dropbox metadata to tables"""
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


class DropboxDB:
    """Class to handle database operations for Dropbox metadata."""

    def __init__(self, host: str, port: int, db_name: str, user: str, password: str):
        try:
            connection_string = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
            self.engine = create_engine(connection_string)
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Database connection error: {e}") from e

    def upsert_dropbox_folder(self, folder) -> None:
        """
        Upsert a Dropbox folder into the database. 
        If the folder already exists, update its information.
        """
        query = """
            INSERT INTO dropbox_folder (
                folder_id, folder_name, parent_shared_folder_id, path_display, path_lower,
                preview_url, property_groups, shared_folder_id
            ) VALUES (
                :id, :name, :parent_shared_folder_id, :path_display, :path_lower,
                :preview_url, :property_groups, :shared_folder_id
            )
            ON CONFLICT (folder_id) DO UPDATE SET
                folder_name = EXCLUDED.folder_name,
                parent_shared_folder_id = EXCLUDED.parent_shared_folder_id,
                path_display = EXCLUDED.path_display,
                path_lower = EXCLUDED.path_lower,
                preview_url = EXCLUDED.preview_url,
                property_groups = EXCLUDED.property_groups,
                shared_folder_id = EXCLUDED.shared_folder_id
        """
        try:
            with self.engine.connect() as conn:
                params = {
                    'id': folder.id,
                    'name': folder.name,
                    'parent_shared_folder_id': folder.parent_shared_folder_id,
                    'path_display': folder.path_display,
                    'path_lower': folder.path_lower,
                    'preview_url': folder.preview_url,
                    'property_groups': folder.property_groups,
                    'shared_folder_id': folder.shared_folder_id
                }
                conn.execute(text(query), params)
                conn.commit()
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Database operation error: {e}") from e

    def upsert_dropbox_file(self, file) -> None:
        """
        Upsert a Dropbox file into the database.
        If the file already exists, update its information.
        """
        query = """
            INSERT INTO dropbox_file (
                id, file_extension, client_modified, content_hash,
                export_info, file_lock_info, has_explicit_shared_members,
                is_downloadable, media_info, file_name, parent_shared_folder_id,
                path_display, path_lower, preview_url, property_groups, rev,
                server_modified, size, symlink_info
            ) VALUES (
                :id, :file_extension, :client_modified, :content_hash,
                :export_info, :file_lock_info, :has_explicit_shared_members,
                :is_downloadable, :media_info, :file_name, :parent_shared_folder_id,
                :path_display, :path_lower, :preview_url, :property_groups, :rev,
                :server_modified, :size, :symlink_info
            )
            ON CONFLICT (id) DO UPDATE SET
                file_extension = EXCLUDED.file_extension,
                client_modified = EXCLUDED.client_modified,
                content_hash = EXCLUDED.content_hash,
                export_info = EXCLUDED.export_info,
                file_lock_info = EXCLUDED.file_lock_info,
                has_explicit_shared_members = EXCLUDED.has_explicit_shared_members,
                is_downloadable = EXCLUDED.is_downloadable,
                media_info = EXCLUDED.media_info,
                file_name = EXCLUDED.file_name,
                parent_shared_folder_id = EXCLUDED.parent_shared_folder_id,
                path_display = EXCLUDED.path_display,
                path_lower = EXCLUDED.path_lower,
                preview_url = EXCLUDED.preview_url,
                property_groups = EXCLUDED.property_groups,
                rev = EXCLUDED.rev,
                server_modified = EXCLUDED.server_modified,
                size = EXCLUDED.size,
                symlink_info = EXCLUDED.symlink_info;
        """
        file_extension = file.name.split('.')[-1] if '.' in file.name else None

        try:
            with self.engine.connect() as conn:
                params = {
                    'id': file.id,
                    'file_extension': file_extension,
                    'client_modified': file.client_modified,
                    'content_hash': file.content_hash,
                    'export_info': file.export_info,
                    'file_lock_info': file.file_lock_info,
                    'has_explicit_shared_members': file.has_explicit_shared_members,
                    'is_downloadable': file.is_downloadable,
                    'media_info': file.media_info,
                    'file_name': file.name,
                    'parent_shared_folder_id': file.parent_shared_folder_id,
                    'path_display': file.path_display,
                    'path_lower': file.path_lower,
                    'preview_url': file.preview_url,
                    'property_groups': file.property_groups,
                    'rev': file.rev,
                    'server_modified': file.server_modified,
                    'size': file.size,
                    'symlink_info': file.symlink_info
                }
                conn.execute(text(query), params)
                conn.commit()
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Database operation error: {e}") from e

    def close(self):
        """Close the database connection."""
        try:
            self.engine.dispose()
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Database close error: {e}") from e
