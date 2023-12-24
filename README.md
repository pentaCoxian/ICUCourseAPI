# ICU Course search API

This is an fastAPI code that scrapes the whole course offerings made by ICU.
ICU email credentials is needed for this to work but also please keep in mind that the data should only ne used for services targetted to ICU students.
When using the data, please impliment a way to verify ICU student status.

For a faster version for this API, there is a version 2 but access to it is limited. If needed, consult with @pentaCoxian. V2 also can get ELA classrooms data as well as providing a summary of each course. the aim of V2 is to get under 0.02s for each full-text search and v1 is intended for couse offerings search.

This code is intended to be used in conjunction with (ICU course API)[https://github.com/pentaCoxian/ICUCourseAPI].


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

> [!WARNING]
> If the above doesn't work, try `sudo apt-get install libmariadb3 libmariadb-dev`

```
cd ./icuCourseAPI
python3.11 -m venv venv

source venv/bin/activate
pip install fastapi "uvicorn[standard]" sqlalchemy python-dotenv mariadb "python-jose[cryptography]" "passlib[bcrypt]" gunicorn
```

Finally, for development use the `--reload` prefix for hot reload. Use of gunicorn to spawn workers and adding the service to systemd are also highly recommended for production.

```
uvicorn sqlapp.main:app --reload
```

> [!TIP]
> When using this code in production, add (course syllabus scrape)[https://github.com/pentaCoxian/ICUCourseScrape] to a cron job and making nginx a reverse proxy might be good.

