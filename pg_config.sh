apt-get -qqy update
DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" upgrade
apt-get -qqy install postgresql python-psycopg2
apt-get -qqy install python-sqlalchemy
apt-get -qqy install python-pip
python -m pip
pip install werkzeug==0.8.3
pip install flask==0.9
pip install requests
pip install httplib2
pip install authlib==0.10
pip install google-api-python-client
pip install google-auth
