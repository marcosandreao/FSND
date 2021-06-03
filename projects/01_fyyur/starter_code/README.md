## Development Setup

1. **Initialize and activate a virtualenv using:**
```
python -m virtualenv env
source env/bin/activate
```
>**Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:
```
source env/Scripts/activate
```

2. **Install the dependencies:**
```
pip install -r requirements.txt
```

3. **Envs:**
```
export FLASK_APP=fyyur
export FLASK_ENV=development # enables debug mode
```
4. **Setup database:**
4.1. **Create database and user:**
```
create user fyyur with encrypted password 'fyyur';
grant all privileges on database fyyur to fyyur;
```
4.2. **Migrate:**
```
flask db upgrade
```
5. **RUN:**
```
flask run
```
6. **Verify on the Browser**<br>
Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000) 

