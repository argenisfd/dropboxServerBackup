Python Application to create backup into dropbox account


#Instalación

##Inatalar Git

	sudo apt-get install git-core

##Clonar el repositorio
Ante de clonar el repositorio debe ubicarse en la carpeta donde se va a hacer la inatalción. Para este ejemplo usaremos la carpeta come del usuario actual

	cd ~

Ahora hacemos clone del proyecto con git

	git clone https://github.com/argenisfd/dropboxServerBackup.git

esto creará la carpeta `dropboxServerBackup` ingresamos a ella:

	cd dropboxServerBackup

hacemos una copia del archivo `paramaters_dist.py` con el nombre `parameters.py`

	cp  paramaters_dist.py parameters.py

y modificamos el contenido del nuevo archivo creado `parameters.py`

* **dropbox.token:** token de la api de dropbox
* **dropbox.sql_backup_folder:** carpeta donde se guardarán los backups (en dropbox) 
 
	#paramaters.py
	parameters={
           "dropbox":{
                      "token":"--dropbox application token--",
                      "sql_backup_folder":"/sql_backup/"
                      },
           "databases":[
                        { 
                         "host": "localhost",
                         "port": "3306",
                         "user":"",
                         "password":"",
                         "name":"database-1"
                         },
                        { 
                         "host": "localhost",
                         "port": "3306",
                         "user":"",
                         "password":"",
                         "name":"database-1"
                         }
                        ],
           "directory_backup":[],
           
           }
