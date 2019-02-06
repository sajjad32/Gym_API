# Gym_API
iman gym api

pip3 install virtualenv

virtualenv venv

cd venv/scripts

activate

pip install -r requirements.txt

create new database in phpmyadmin call "gym"

python manage.py makemigrations

python manage.py migrate

python manage.py runserver
