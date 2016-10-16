from parameters import parameters
import os
from datetime import datetime
from dropbox_sync import DropboxSync
import json
import dropbox


CURRENT_FOLDER= os.path.dirname(os.path.abspath(__file__))
TEMP_FOLDER=CURRENT_FOLDER + "/temp/"
try:
    os.stat(TEMP_FOLDER)
except:
    os.mkdir(TEMP_FOLDER)       

db_info=[]
db_old_interaction={}
for db in parameters.get("databases"):
    dropbox_backup_strategy=db.get("dropbox_backup_strategy") or "normal"
    db_file="%s_%s.sql" % (db["name"], str(datetime.now().isoformat()).replace(" ","_").replace(":","_").replace(".","_") );
    #db_file="backup_%s_%s.sql" % (db["name"], "2016" )
    os.system("mysqldump -h%s -P%s -u%s -p%s --opt %s > %s" % (db["host"], db["port"], db["user"], db["password"], db["name"],TEMP_FOLDER+db_file))
    db_info.append({ "sql_file_name": db_file,"db_name": db["name"], "db_host": db["host"],"dropbox_backup_strategy": dropbox_backup_strategy } )
    

compress_files=[]
for i, info in enumerate(db_info):
    compress_file="%s.tar.gz"% (info["sql_file_name"],)
    os.system("cd %s && tar -czvf %s %s "% (TEMP_FOLDER,compress_file,info["sql_file_name"]))
    db_info[i]["compress_file"]=compress_file
    compress_files.append(compress_file)
    
os.system("cd %s" % (CURRENT_FOLDER,))
    

dropboxSync= DropboxSync(parameters.get("dropbox").get("token"))
for i,info in enumerate(db_info):
    dropbox_file_path=parameters.get("dropbox").get("sql_backup_folder")+info["compress_file"]
    db_info[i]["dropbox_file_path"]=dropbox_file_path
    dropboxInfo= dropboxSync.send(TEMP_FOLDER+info["compress_file"],dropbox_file_path)
    db_info[i]["file_size"]=dropboxInfo.size
     
os.system("rm -f %s*"%(TEMP_FOLDER,))

last_transaction_data = None
try:
    last_transaction_file = open("last_transaction.json","r")
    last_transaction_data = json.loads(last_transaction_file.read())
    last_transaction_file.close()
except:
    pass

if None is not last_transaction_data:
    for info in db_info:
        key= "%s_%s"%(info["db_host"], info["db_name"]) 
        if key in last_transaction_data['dbs'].keys():
            last_info = last_transaction_data['dbs'][key]
            old_dropbox_file_path=last_info['dropbox_file_path']
            if "replace" == info["dropbox_backup_strategy"]:
                if len(str(old_dropbox_file_path)) > 2:
                    try:
                        dropboxSync.delete(old_dropbox_file_path)
                    except:
                        print "no se pudo eliminar %s", (old_dropbox_file_path, )
            elif "replace_if_gt_or_eq" == info["dropbox_backup_strategy"]:
                if info["file_size"] >= last_info['file_size']:
                    try:
                        dropboxSync.delete(old_dropbox_file_path)
                    except:
                        print "no se pudo eliminar %s", (old_dropbox_file_path, )
             
    
new_last_transaction_file = open("last_transaction.json","w")
new_last_transaction_data={"dbs": {}};
for info in db_info:
    new_last_transaction_data["dbs"]["%s_%s"%(info["db_host"], info["db_name"])]=info
new_last_transaction_file.write(json.dumps(new_last_transaction_data, indent=4))
new_last_transaction_file.close()

