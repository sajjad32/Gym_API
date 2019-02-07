# Gym_API
iman gym api

virtualenv venv

cd venv/scripts

activate

pip install -r requirements.txt

create new database in phpmyadmin call "gym" and set the encoding to "utf8_bin"

python manage.py makemigrations

python manage.py migrate

python manage.py runserver
