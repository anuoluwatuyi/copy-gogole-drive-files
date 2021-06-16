# Import PyDrive and associated libraries.
# This only needs to be done once per notebook.
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials


# Authenticate and create the PyDrive client.
# This only needs to be done once per notebook.
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

folderID = 'YOUR FOLDER ID' #the folder to be copied from
folderID2 = 'YOUR FOLDER ID' #the flder to be copied to

# create a copy files funtion that can run recursively
def copyFiles(folderID):
  
  # list all folders in the first/parent folder
  folders = drive.ListFile({'q': "'"+folderID+"' in parents and mimeType = 'application/vnd.google-apps.folder'"}).GetList()
  
  # List all csv files in the folder
  # "mimeType = 'text/csv'" lists all CSV files in the folder
  # For more Search query references go to:
  # https://developers.google.com/drive/v2/web/search-parameters
  files = drive.ListFile({'q': "'"+folderID+"' in parents and mimeType = 'text/csv'"}).GetList()
  
  # copy all csv files in the parent folder
  for file in files:
    drive.auth.service.files().copy(fileId=file['id'], body={"parents": [{"kind": "drive#fileLink", "id": folderID2,'title': file['title']}]}).execute()
    print("copied "+file['title']+" to new folder")
  
  # get all children folders in the parent folder and all the copyFiles funtion on each folder id
  for folder in folders:
    print("opened "+folder['title']+" folder")
    copyFiles(folder['id'])


copyFiles(folderID)
