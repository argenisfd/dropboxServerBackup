import dropbox
import sys
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
class DropboxSync(object):
    token=None
    drobox=None
    def __init__(self, token):
        self.token=token
        self.dbx = dropbox.Dropbox(self.token)
        # Check that the access token is valid
        try:
            self.dbx.users_get_current_account()
        except AuthError as err:
            sys.exit("ERROR: Invalid access token; try re-generating an access token from the app console on the web.")

        
        
    def send(self,file_from, file_to):
        with open(file_from, 'rb') as f:
            # We use WriteMode=overwrite to make sure that the settings in the file
            # are changed on upload
            print("Uploading " + file_from + " to Dropbox as " + file_to + "...")
            try:
                self.dbx.files_upload(f, file_to, mode=WriteMode('overwrite'))
            except ApiError as err:
                # This checks for the specific error where a user doesn't have
                # enough Dropbox space quota to upload this file
                if (err.error.is_path() and
                        err.error.get_path().error.is_insufficient_space()):
                    sys.exit("ERROR: Cannot back up; insufficient space.")
                elif err.user_message_text:
                    print(err.user_message_text)
                    sys.exit()
                else:
                    print(err)