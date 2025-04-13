CREATE TABLE IF NOT EXISTS dropbox_folder (
    folder_id TEXT PRIMARY KEY,
    folder_name TEXT NOT NULL,
    parent_shared_folder_id TEXT,
    path_display TEXT NOT NULL,
    path_lower TEXT NOT NULL,
    preview_url TEXT,
    property_groups TEXT,
    shared_folder_id TEXT,
    sharing_info  TYPE JSONB USING sharing_info::JSONB
);

ALTER TABLE dropbox_folder OWNER TO dropbox_indexer;

CREATE INDEX IF NOT EXISTS idx_dropbox_folder_path_display ON dropbox_folder (path_display);
CREATE INDEX IF NOT EXISTS idx_dropbox_folder_path_lower ON dropbox_folder (path_lower);

CREATE TABLE IF NOT EXISTS dropbox_file (
    id TEXT PRIMARY KEY,
    file_extension TEXT,
    client_modified TIMESTAMP,
    content_hash TEXT,
    export_info TEXT,
    file_lock_info TEXT,
    has_explicit_shared_members BOOLEAN,
    is_downloadable BOOLEAN,
    media_info TEXT,
    file_name TEXT,
    parent_shared_folder_id TEXT,
    path_display TEXT,
    path_lower TEXT,
    preview_url TEXT,
    property_groups TEXT,
    rev TEXT,
    server_modified TIMESTAMP,
    sharing_info TEXT,
    size BIGINT,
    symlink_info TEXT
);

ALTER TABLE dropbox_file OWNER TO dropbox_indexer;

CREATE INDEX IF NOT EXISTS idx_dropbox_file_path_display ON dropbox_file (path_display);
CREATE INDEX IF NOT EXISTS idx_dropbox_file_path_lower ON dropbox_file (path_lower);
CREATE INDEX IF NOT EXISTS idx_dropbox_file_client_modified ON dropbox_file (client_modified);
CREATE INDEX IF NOT EXISTS idx_dropbox_file_server_modified ON dropbox_file (server_modified);
CREATE INDEX IF NOT EXISTS idx_dropbox_file_file_name ON dropbox_file (file_name);
CREATE INDEX IF NOT EXISTS idx_dropbox_file_file_extension ON dropbox_file(file_extension);