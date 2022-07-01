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
