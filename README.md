# Dropbox Indexer

This project indexes metadata of files and folders from your Dropbox account and saves it into two PostgreSQL tables. It allows you to query and analyze your Dropbox content efficiently.

## Features
- Fetches metadata of files and folders from Dropbox.
- Stores metadata in two PostgreSQL tables: one for files and one for folders.
- Provides a foundation for querying Dropbox content using SQL.

## Prerequisites
1. **Python Environment**: Ensure you have Python 3.10+ installed.
2. **PostgreSQL Database**: Set up a PostgreSQL database to store the metadata.
3. **Dropbox App**: Create a private app in Dropbox to access your account's metadata.

## Steps to Set Up Your Dropbox App
1. **Create the App**:
   - Go to the [Dropbox App Console](https://www.dropbox.com/developers/apps).
   - Click "Create app".
   - Choose "Scoped Access" and select "Full Dropbox" access type.
   - Name your app.

2. **Configure Permissions**:
   - In your app's settings, navigate to the "Permissions" tab.
   - Enable the necessary scope:
     - `files.metadata.read`

3. **Generate Access Token**:
   - In the "OAuth 2" section of your app's settings, click "Generate" to create an access token.
   - Use this token in your `.env` file to authenticate API requests.

## Environment Variables
The script requires the following environment variables, which should be defined in a `.env` file:

- `DROPBOX_ACCESS_TOKEN`: The access token generated from your Dropbox app.
- `DB_HOST`: The hostname of your PostgreSQL database.
- `DB_PORT`: The port number of your PostgreSQL database.
- `DB_NAME`: The name of your PostgreSQL database.
- `DB_USER`: The username for your PostgreSQL database.
- `DB_PASSWORD`: The password for your PostgreSQL database.

An example `.env` file is provided as `.env-example` in this repository.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/pypopsjf/dropbox-indexer.git
   cd dropbox-indexer

## Querying the database - Examples

### List all mp3 files on your Dropbox

```
   SELECT file_name
         ,path_display
         ,file_extension
         ,client_modified
     FROM dropbox_file 
    WHERE file_extension = 'mp3'
 ORDER BY path_display
```

### List all folder where folder name contains Django

```
	SELECT folder_id 
	      ,folder_name
		  ,path_display
	  FROM public.dropbox_folder 
	 WHERE path_display like '%Django%'
  ORDER BY path_display;
```

### List folder exactly 2 levels deep

```
   SELECT folder_id
         ,folder_name
         ,path_display
     FROM dropbox_folder
    WHERE path_display ~ '^/[^/]+/[^/]+$'
 ORDER BY path_display;
```

## To-Do / Planned Enhancements

Here are some planned improvements for future versions of this project:

1. **Save `sharing_info` in `dropbox_folder`**:
   - Fix the code to properly serialize and store the `sharing_info` field in the `dropbox_folder` table.

2. **Add Folder Hierarchy**:
   - Introduce a `parent_id` column in the `dropbox_folder` table to represent folder hierarchy.
   - This will allow `WITH RECURSIVE` queries.

3. **Add Foreign Key to `dropbox_file`**:
   - Add a `folder_id` foreign key column to the `dropbox_file` table to link files to their parent folders.

4. **Improve Query Examples**:
   - Add more SQL query examples to demonstrate how to use the database effectively (e.g., hierarchical queries, advanced filtering).

5. **Docker Support**:
   - Add a `Dockerfile` and `docker-compose.yml` to simplify deployment and setup.
