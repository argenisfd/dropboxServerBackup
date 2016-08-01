from parameters import parameters
import os
from datetime import datetime
from dropbox_sync import DropboxSync



CURRENT_FOLDER= os.path.dirname(os.path.abspath(__file__))
TEMP_FOLDER=CURRENT_FOLDER + "/temp/"
try:
    os.stat(TEMP_FOLDER)
except:
    os.mkdir(TEMP_FOLDER)       

db_files=[]
for db in parameters.get("databases"):
    db_file="%s_%s.sql" % (db["name"], str(datetime.now().isoformat()).replace(" ","_").replace(":","_").replace(".","_") );
    #db_file="backup_%s_%s.sql" % (db["name"], "2016" )
    os.system("mysqldump -h%s -P%s -u%s -p%s --opt %s > %s" % (db["host"], db["port"], db["user"], db["password"], db["name"],TEMP_FOLDER+db_file))
    db_files.append(db_file)

compress_files=[]
for file in db_files:
    compress_file="%s.tar.gz"% (file,)
    os.system("cd %s && tar -czvf %s %s "% (TEMP_FOLDER,compress_file,file))
    compress_files.append(compress_file)
    
os.system("cd %s" % (CURRENT_FOLDER,))
    

dropboxSync= DropboxSync(parameters.get("dropbox").get("token"))
for tar_file in compress_files:
    dropboxSync.send(TEMP_FOLDER+tar_file,parameters.get("dropbox").get("sql_backup_folder")+tar_file)

os.system("rm -f %s*"%(TEMP_FOLDER,))