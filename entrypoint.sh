#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset


postgres_ready() {
python << END
import sys
from urllib.parse import urlparse
import psycopg2
try:
    url = urlparse("${DATABASE_URL:-psql://postgres:postgres@db:5432/postgres}")

    psycopg2.connect(
        dbname=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port,
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)

END
}


until postgres_ready; do
  >&2 echo 'Waiting for PostgreSQL to become available...'
  sleep 1
done
>&2 echo 'PostgreSQL is available'

python manage.py migrate
python manage.py collectstatic --noinput

cat <<EOF | python manage.py shell
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.filter(username="${DJANGO_SUPERUSER_USERNAME:-admin}").first()
if not user:
    user = User.objects.create_superuser(
       "${DJANGO_SUPERUSER_USERNAME:-admin}",
       "${DJANGO_SUPERUSER_EMAIL:-admin@admin.com}",
       "${DJANGO_SUPERUSER_PASSWORD:-password}")
    print(f'User "{user.username}" created')
else:
    print(f'User "{user.username}" exists already')
EOF

exec "$@"
