from parameters import parameters
import os
from datetime import datetime
from dropbox_sync import DropboxSync

db_files=[]
for db in parameters.get("databases"):
    db_file="%s_%s.sql" % (db["name"], str(datetime.now().isoformat()).replace(" ","_").replace(":","_").replace(".","_") );
    #db_file="backup_%s_%s.sql" % (db["name"], "2016" )
    os.system("mysqldump -u%s -p%s --opt %s > temp/%s" % (db["user"],db["password"],db["name"],db_file))
    db_files.append(db_file)

compress_files=[]    
for file in db_files:
    compress_file="%s.tar.gz"% (file,)
    os.system("tar -czvf temp/%s %s"% (compress_file,file))
    compress_files.append(compress_file)
    

dropboxSync= DropboxSync(parameters.get("dropbox").get("token"))
for tar_file in compress_files:
    dropboxSync.send("temp/"+tar_file,parameters.get("dropbox").get("sql_backup_folder")+tar_file)

os.system("rm -f ./temp/*")