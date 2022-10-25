# Star Wars Django

Star Wars Django is an API based on **Django 3.1** , **DRF 3.12** and **python 3.9**. Database used to the project is 
**Postgresql 14.5**.


## Local installation
In order to use the project in a local enviroment, you should create a python enviroment where you install all 
requirements. You can see [docs](https://docs.python.org/3.9/library/venv.html) that explain the proccess. When you have 
created your python enviroment, you have to use the following commands:

```shell
pip install -r requirements.txt
```
- Migrate data
```shell
python manage.py migrate
```
- [Optional] Run test
```shell
python manage.py test
```
- Load initial data to database
```shell
python manage.py loaddata movies.json
```
```shell
python manage.py loaddata planets.json
```
```shell
python manage.py loaddata people.json
```
- Create superuser to use API
```shell
python manage.py createsuperuser
```
- Run server
```shell
python manage.py runserver
```

## Extra resources
If you desire to use **Postman**, you can use the following 
[collection](https://www.postman.com/orbital-module-astronomer-90282829/workspace/start-wars-api/overview) which will
help you in using API.