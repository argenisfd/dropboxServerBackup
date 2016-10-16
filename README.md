Python Application to create backup into dropbox account

#Requerimientos
python >= 2.7 
git 
pip 
virtualenv (opcional) 

#Instalación

##Instalar Git

	sudo apt-get install git-core



##Instalar pip
Para mayor documentación ir a la [documentación](http://www.saltycrane.com/blog/2010/02/how-install-pip-ubuntu/)

	sudo apt-get install python-setuptools python-dev build-essential 


##Instalar virtualenv
Para mayor información visitar esta [web](http://rukbottoland.com/blog/tutorial-de-python-virtualenv/).
	sudo pip install virtualenv 


##Clonar el repositorio
Ante de clonar el repositorio debe ubicarse en la carpeta donde se va a hacer la instalación. Para este ejemplo usaremos la carpeta come del usuario actual
	cd ~

Ahora hacemos clone del proyecto con git

	git clone https://github.com/argenisfd/dropboxServerBackup.git

esto creará la carpeta `dropboxServerBackup` ingresamos a ella:

	cd dropboxServerBackup


## Instalando dependenncias con pip y virtualenv
	
	virtualenv ./env 

El comando anterior creará la carpeta `env/`.

Ahora activaremos el enviroment (es necesario hacer esto cada vez que se quiera correr el programa)

	source ./env/bin/activate

Instalamos todas las dependencias

	pip install -r requirements.txt 


Hacemos una copia del archivo `paramaters_dist.py` con el nombre `parameters.py`

	cp  paramaters_dist.py parameters.py

y modificamos el contenido del nuevo archivo creado `parameters.py`

* **dropbox.token:** token de la api de dropbox.
* **dropbox.sql_backup_folder:** carpeta donde se guardarán los backups (en dropbox).
* **databases:** aquí puede ir una lista de bases de datos a las que se les quiere hacer backup.
* **databases.host:** IP o dominio del servidor de base de datos.
* **databases.port:** Puerto del servidor de base de datos.
* **databases.user:** Usuario del servidor de base de datos, verificar el el usuario tenga acceso a la base de datos a la que se le desea hacer el backup.
* **databases.password:** Password del usuario de base de datos.
* **databases.name:** Nombre de la base de datos a la que se le hará el backup.
* **databases.dropbox_backup_strategy (opcional):** estrategia para el almacenamiento en dropbox (**normal** = crea un nuevo archivo, **replace** = crea el nuevo archivo y elimina el anterior, **replace_if_gt_or_eq** = Genera el nuevo archivo y elimina el anterior si es mas pequeño o igual al nuevo).
* **directory_backup:** Listado de rutas a las que se le desea hacer el backup, esto no está desarrollado aún, espero colaboradores :).


```python
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
                     "name":"database-1",
                     "dropbox_backup_strategy": "replace_if_gt_or_eq"
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
```

Una vez configurado correctamente los parametros probamos

	python backup_command.py
	
Si todo funciona bien vamos al siguiente paso.

##Configurar Cron

	crontab -e

Y editamos el archivo de cron, si no pregunta el editor a usar, preferiblemente usar `nano`. y agregamos esta linea al final del archivo ([Saber mas sobre crontab](http://blog.desdelinux.net/cron-crontab-explicados/) [herramienta para crear crontab](http://crontab-generator.org/) ).

	0 3 1 * * PYTHONPATH=/RUTA-HASTA-LA-CARPETA-ENV-CREADA/lib/python2.7/site-packages/ python /RUTA-HASTA-LA-CARPETA-DE-INSTALACION/backup_command.py 
  
Con esta linea el backup se ejecutará todos los días a las 3:01 am.

Para probar si el comando ingresado anteriormente funciona bien lo probamos directamente en la consola.
	
Primero desactivamos el virtualenv

	deactivate

ejecutamos 

	PYTHONPATH=/RUTA-HASTA-LA-CARPETA-ENV-CREADA/lib/python2.7/site-packages/ python /RUTA-HASTA-LA-CARPETA-DE-INSTALACION/backup_command.py

