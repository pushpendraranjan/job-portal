from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'service_account.json'
FOLDER_ID = '1EWwlUO0l5MYIE9MQwpQktL3bS_bI1MFT'

# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaIoBaseUpload

# SCOPES = ['https://www.googleapis.com/auth/drive']
# SERVICE_ACCOUNT_FILE = 'service_account.json'
# FOLDER_ID = '1EWwlUO0l5MYIE9MQwpQktL3bS_bI1MFT'

def upload_to_drive(upload_file):
    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=SCOPES
        )

        service = build('drive', 'v3', credentials=creds)

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
        ).execute()                      #error

        file_id = uploaded.get('id')

        service.permissions().create(
            fileId=file_id,
            body={'type': 'anyone', 'role': 'reader'}
        ).execute()  

        return f"https://drive.google.com/file/d/{file_id}/view"

    except Exception as e:
        print("Drive error:", e)
        raise e   # VERY IMPORTANT                    error

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
