#! /usr/bin/env sh
set -eu

echo "Waiting for postgres connection"

while ! nc -z database 5432; do
    sleep 0.1
done

echo "PostgreSQL started"

# Execute alembic migration during start up if DEV_MODE is set
# see: https://pythonspeed.com/articles/schema-migrations-server-startup/
# if [ -v DEV_MODE ]; then
#     echo "Executting alembic migration"
#     alembic upgrade head
# else
#     echo "Skiping alembic migration"
# fi

# We are executting the migration on start up,
# if this turn out to be problematic use the solution above.
echo "Executting alembic migration"
alembic upgrade head

exec uvicorn app.main:app --reload --reload-dir app --proxy-headers --port 80 --host 0.0.0.0 --log-level warning
