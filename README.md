## Install

install python3.11 (ubuntu20.04)

```
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11 python3.11-dev python3.11-venv
```

check python and pip versions

```
python3.11 -V
python3.11 -m pip -V
```

we use a virtual enviroment for development.

install maradb connector c CS package. ([Install CS package](https://mariadb.com/docs/connect/programming-languages/c/install/))

> [!NOTE]
> If the above doesn't work, try `sudo apt-get install libmariadb3 libmariadb-dev`

```
cd ./icuCourseAPI
python3.11 -m venv venv

source venv/bin/activate
pip install fastapi
pip install "uvicorn[standard]"
pip install sqlalchemy python-dotenv mariadb
```

Finally,

```
uvicorn sqlapp.main:app --reload
```

> [!TIP]
> When deploying as a service, consider using gunicorn to make runners as well as adding a reverce proxy.


