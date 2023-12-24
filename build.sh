#!/usr/bin/env bash
set -o errexit

echo "Home dir ------> $HOME"

#Download the SSL certificate
curl --create-dirs -o $HOME/.postgresql/root.crt 'https://cockroachlabs.cloud/clusters/442c70b5-9424-4f37-9ee4-c81f59229538/cert'

#Download the cockroachlab dependencies for sqlalchemy
pip3 install git+https://github.com/felipediel/python-broadlink.git@patch-24 sqlalchemy-cockroachdb --force-reinstall --no-deps

pip install -r requirements.txt
alembic upgrade head


# Below is a sample build file found on https://community.render.com/t/postgresql-root-crt-missing/7347 


# #!/usr/bin/env bash
# set -o errexit

# mkdir -p /opt/render/.postgresql/
# if [ ! -f /opt/render/.postgresql/root.crt ]; then
#     cp /etc/secrets/postgresql-root.crt /opt/render/.postgresql/root.crt
# fi

# pip install -U pip
# pip install -r requirements.txt
# python manage.py collectstatic --no-input
# mkdir -p staticfiles
# python manage.py migrate