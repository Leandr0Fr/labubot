import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
    
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_service():

    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    try:
        service = build("gmail", "v1", credentials=creds)
        return service

    except HttpError as error:
        print(f"An error occurred: {error}")

def get_code(service) -> str:
        results = service.users().messages().list(userId='me', maxResults=1).execute()
        messages = results.get('messages', [])

        msg = service.users().messages().get(userId='me', id=messages[0]['id']).execute()
        subject = get_header(msg, 'Subject')
        code = subject[-6:len(subject)]
        
        return code

def get_header(message, header_name):
    headers = message['payload'].get('headers', [])
    for header in headers:
        if header['name'] == header_name:
            return header['value']
    return None