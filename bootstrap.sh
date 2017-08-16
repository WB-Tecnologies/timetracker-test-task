#!/usr/bin/env bash

sudo sh -c 'echo "deb http://repo.postgrespro.ru/pgpro-9.6/debian $(lsb_release -cs) main" > /etc/apt/sources.list.d/postgrespro.list'
wget --quiet -O - http://repo.postgrespro.ru/pgpro-9.6/keys/GPG-KEY-POSTGRESPRO |sudo apt-key add -

sudo apt-get update -y

sudo apt-get install -y python 3.5.3 python-pip

pip install virtualenv


    # Install Python requirements
sudo -u vagrant virtualenv --python=python3 /home/vagrant/.virtualenvs/tt_env
sudo -u vagrant PYTHONUNBUFFERED=1 sh -c ". /home/vagrant/.virtualenvs/tt_env/bin/activate && pip install -r /timetracker/timetracker/requirements.txt"

    # Install postgres and create db
sudo apt-get install -y postgrespro-9.6 postgrespro-contrib-9.6 postgrespro-plperl-9.6 postgrespro-plpython-9.6 postgrespro-plpython3-9.6 postgrespro-pltcl-9.6
su - postgres -c "createuser -s vagrant"
su - vagrant -c "createdb timetrackerdb"

   # Create a login script to create the virtualenv and Run server
    cat > /home/vagrant/.bash_profile <<INIT
export WORKON_HOME=/home/vagrant/.virtualenvs
mkdir -p /home/vagrant/.virtualenvs
source /home/vagrant/.virtualenvs/tt_env/bin/activate
 # Run run run
python /timetracker/timetracker/manage.py migrate
python /timetracker/timetracker/manage.py runserver 0.0.0.0:8000
INIT
