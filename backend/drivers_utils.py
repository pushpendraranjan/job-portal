# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaIoBaseUpload

# SCOPES = ['https://www.googleapis.com/auth/drive']
# SERVICE_ACCOUNT_FILE = 'service_account.json'
# FOLDER_ID = '1EWwlUO0l5MYIE9MQwpQktL3bS_bI1MFT'

# # from google.oauth2 import service_account
# # from googleapiclient.discovery import build
# # from googleapiclient.http import MediaIoBaseUpload

# # SCOPES = ['https://www.googleapis.com/auth/drive']
# # SERVICE_ACCOUNT_FILE = 'service_account.json'
# # FOLDER_ID = '1EWwlUO0l5MYIE9MQwpQktL3bS_bI1MFT'
# creds = service_account.Credentials.from_service_account_file(
#     SERVICE_ACCOUNT_FILE, 
#     scopes=SCOPES
# )
# drive_service = build('drive', 'v3', credentials=creds)

# def upload_to_drive(upload_file):
#     try:
#         creds = service_account.Credentials.from_service_account_file(
#             SERVICE_ACCOUNT_FILE,
#             scopes=SCOPES
#         )

#         service = build('drive', 'v3', credentials=creds)

#         file_metadata = {
#             'name': upload_file.filename,
#             'parents': [FOLDER_ID]
#              }

#         media = MediaIoBaseUpload(
#             upload_file.file,
#             mimetype=upload_file.content_type,
#             resumable=True
#         )

#         uploaded = service.files().create(
#             body=file_metadata,
#             media_body=media,
#             fields='id',
#             supportsAllDrives=True, # Even for personal drives, this helps
#             supportsTeamDrives=True
#         ).execute()                      #error

#         file_id = uploaded.get('id')

#         service.permissions().create(
#             fileId=file_id,
#             body={'type': 'anyone', 'role': 'reader'}
#         ).execute()  

#         return f"https://drive.google.com/file/d/{file_id}/view"

#     except Exception as e:
#         print("Drive error:", e)
#         raise e   # VERY IMPORTANT                    error

# def upload_to_drive(upload_file):
#     try:
#         creds = service_account.Credentials.from_service_account_file(
#             SERVICE_ACCOUNT_FILE, scopes=SCOPES
#         )
#         service = build('drive', 'v3', credentials=creds)

#         file_metadata = {
#             'name': upload_file.filename,
#             'parents': [FOLDER_ID]
#         }

#         media = MediaIoBaseUpload(
#             upload_file.file,
#             mimetype=upload_file.content_type,
#             resumable=True
#         )

#         uploaded = service.files().create(
#             body=file_metadata,
#             media_body=media,
#             fields='id'
#         ).execute()

#         file_id = uploaded.get('id')

#         # Make it public so admin can view
#         service.permissions().create(
#             fileId=file_id,
#             body={'type': 'anyone', 'role': 'reader'}
#         ).execute()

#         return f"https://drive.google.com/file/d/{file_id}/view"

#     except Exception as e:
#         print("Drive error:", e)
#         return None

        
#         return file_url

#     except Exception as e:
#         print("Google Drive Upload Error:", e)
#         raise e


# def upload_to_drive(upload_file):
#     try:
#         creds = service_account.Credentials.from_service_account_file(
#             SERVICE_ACCOUNT_FILE, scopes=SCOPES
#         )
#         service = build('drive', 'v3', credentials=creds)

#         file_metadata = {
#             'name': upload_file.filename,
#             'parents': [FOLDER_ID]
#         }

#         media = MediaIoBaseUpload(
#             upload_file.file,
#             mimetype=upload_file.content_type,
#             resumable=True
#         )

#         uploaded = service.files().create(
#             body=file_metadata,
#             media_body=media,
#             fields='id'
#         ).execute()

#         file_id = uploaded.get('id')

#         # Make it public so admin can view
#         service.permissions().create(
#             fileId=file_id,
#             body={'type': 'anyone', 'role': 'reader'}
#         ).execute()

#         return f"https://drive.google.com/file/d/{file_id}/view"

#     except Exception as e:
#         print("Drive error:", e)
#         return None
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']
TOKEN_FILE = "D://codenscious//job_portal//token.json"  # Generated after OAuth login
FOLDER_ID = '1EWwlUO0l5MYIE9MQwpQktL3bS_bI1MFT'


def get_drive_service():
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds:
        raise Exception("OAuth token.json not found. Run OAuth flow first.")

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)


def upload_to_drive(upload_file):
    try:
        service = get_drive_service()

        file_metadata = {
            'name': upload_file.filename,
            'parents': [FOLDER_ID]
        }

        media = MediaIoBaseUpload(
            upload_file.file,
            mimetype=upload_file.content_type,
            resumable=True
        )

        uploaded = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        file_id = uploaded.get('id')

        # Make file public (view only)
        service.permissions().create(
            fileId=file_id,
            body={'type': 'anyone', 'role': 'reader'}
        ).execute()

        return f"https://drive.google.com/file/d/{file_id}/view"

    except Exception as e:
        print("Drive error:", e)
        raise e
