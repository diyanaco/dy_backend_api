# dy_backend_api
Flask
Restful Api

source ./venv/Scripts/activate


Deployment:
Create a Linode instance.
ssh into root of the newly created instance (get the SSH access)
In root os: update library 
```
yum update -y
sudo yum install epel-release
scp /deployment/__init__.py root@172.104.188.38:/root/diyanaco/__init__.py
```

hehe testing clickup integrations

testing main

# Alembic
alembic revision --autogenerate -m "Added account table"
alembic upgrade head

When creating new link table, alembic won't be able to detect the changes, so need to "flask run" and create the link table first
After the table is created then can do some manipulations on the table and alembic will be able to detect

# SQLAlchemy
query data and session commit must present in the same app context (meaning same function or file)

# Pip Freeze
## To append to existing requirements.txt
pip freeze > requirements.txt
## To create new requirements.txt
pipi freeze -r requirements.txt