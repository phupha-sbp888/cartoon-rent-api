#!/bin/sh

set -e

if [ "$DJANGO_MANAGE_MIGRATE" = 'on' ]; then
    python manage.py migrate
fi

echo "Starting server..."
exec $@
