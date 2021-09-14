## Running Web-app

Clone Repo \
Go into folder(to start backend server) 
```
Create virtual environment 
```
virtualenv env
```
Activate virtual environment(search up for specific OS)
```
source bin/Scripts/activate
```
Install Dependencies
```
pip install -r requirements.txt
```

do all stuff related to Django like migrations and all
```
py manage.py migrate
py manage.py runserver
```

To work with websocket install redis or use docker
```
docker run -d --name redis -p 6379:6379 redis:5
```

Follow-up steps in readme file from frontend folder to start server for frontend

Note
> Configure your database in settings.py \
> create Admin user to view tables on admin page 

### Features to-do List

- [x] Basic Authentication
- [x] Messaging
- [x] Initial Message Retrival
- [x] Changing Users through websocket instead of URL
- [ ] Social Authentications
- [ ] Async Messeging
- [ ] Notifications