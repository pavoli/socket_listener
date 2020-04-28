![](logo.png)
# python_socket ![](https://img.shields.io/badge/python-3.7-blue.svg)
> Console application. It listening sockets, from 9217 to 9223.
>
># PYTHON_SOCKET IS LISTENING PORTS AND RECEIVING INFORMATION FROM REMOTE SERVERS (MES) ABOUT CAR-BODY. SAVE IT INTO DB ORACLE AND THEN SHOW PARSED DATA IN PDP.
# GETTING STARTED
**IMPORTANT:** All packages listed in `requirements.txt`.

## INSTALL
* Install python version 3.7 or later [HERE](https://www.python.org/downloads/)
* Create an [VIRTUAL ENV](https://docs.python.org/3/library/venv.html)
```bash
$ mkdir venv
$ python3 -m venv /path/to/new/virtual/environment
```
* Activate VENV
```bash
$ cd  /path/to/new/virtual/environment
$ cd Scripts/
$ source activate
$ pip install -r requirements.txt
```
--or--
* Install into local PYTHON PACKAGE
```bash
$ pip install -r requirements.txt
```

## PROJECT STRUCTURE
```
app
├── services            
│   ├── 1 cmd           cmd script
│   ├── 2 powershell    powershell script
│   └── 3 registry      input data in registry
├── conf.py             configuration settings
├── create_socket.py    
├── run_socket.py       
├── work_with_db.py     
├── README.rd           this file
└── requirements.txt    
```

## USE APPLICATION AS A SERVICE
* run scripts from folder `app/services` as numbered
    * 1 cmd `run as Administrator`
    * 2 powershell `run as Administrator`
    * 3 registry `run`
* run `services.msc`
* run `<SERVICE NAME>`