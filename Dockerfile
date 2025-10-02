FROM python:3.13-slim

ENV UID=1001
ENV GID=1001
ENV USERNAME=cartoon_book_user
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERACTION=1 \
    POETRY_HOME="/home/$USERNAME/.poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=false

ENV PATH="$POETRY_HOME/bin:$PATH"
ENV DJANGO_MANAGE_MIGRATE=on

# Create group and system user
RUN addgroup --gid $GID $USERNAME \
    && adduser --uid $UID --gid $GID --disabled-password --gecos "" $USERNAME

#  Update and install system dependencies
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
       curl \
       git \
       && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && poetry config virtualenvs.create false \
    && chown -R $UID:$GID /home/$USERNAME/.poetry \
    && apt-get remove -y curl \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/$USERNAME/cartoon_book_rent_app

COPY . .

# Install dependencies
RUN poetry check && poetry install --without dev

RUN python manage.py collectstatic  --no-input --clear \
    && chown -R $UID:$GID . \
    && chmod -R o-rwx,g-wx .\
    && chmod +x docker-entrypoints.sh manage.py \
    && rm -rf poetry.lock pyproject.toml
USER $USERNAME
EXPOSE  8000
ENTRYPOINT ["./docker-entrypoints.sh", "gunicorn", "cartoon_rent_api.wsgi:application", "--bind 0.0.0.0:8000", "--timeout 600", "--preload"]
