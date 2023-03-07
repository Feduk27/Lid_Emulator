import time
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
folder = '1g3bI8UeSR3bhOXRXwzEaPQ6q13fzv4Rn'
log_folder = '10ADImgwKKpN-Cz1JEtS-p7dfp-bfllbs'

def gdrive_upload(filename: str, file_content: str, folder=folder):
    try:
        drive = GoogleDrive(gauth)
        # File delete if it already exists
        file_list = drive.ListFile({'q': f"'{folder}' in parents and trashed=false"}).GetList()
        for file in file_list:
            if file['title'] == filename:
                file.Delete()
        # Сreating new file
        my_file = drive.CreateFile({'parents': [{'id': folder}], 'title': filename})
        my_file.SetContentString(file_content)
        my_file.Upload()
        print(f'File {filename} was uploaded')
    except Exception as ex:
        print(ex)

def gdrive_download(filename: str):
    try:
        drive = GoogleDrive(gauth)
        file_list = drive.ListFile({'q': f"'{folder}' in parents and trashed=false"}).GetList()
        for file in file_list:
            if file['title'] == filename:
                file.GetContentFile(file['title'])
                return f'File {filename} was downloaded'
        return -1
    except Exception as ex:
        print(f'Error {ex}')

def gdrive_delete(filename: str, folder=folder):
    try:
        drive = GoogleDrive(gauth)
        file_list = drive.ListFile({'q': f"'{folder}' in parents and trashed=false"}).GetList()
        for file in file_list:
            if file['title'] == filename:
                file.Delete()
                return f'File {filename} was deleted'
        return -1
    except Exception as ex:
        print(f'Error {ex}')


def main():
    print(gdrive_delete('log_444.txt', log_folder))

if __name__ == '__main__':
    main()