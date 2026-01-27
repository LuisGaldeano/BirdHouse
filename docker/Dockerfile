FROM python:3.14

# Install tools needed for translations
RUN apt-get update && apt-get install -y wget make gettext && apt-get clean
RUN apt-get autoclean

# Prepare work directory
RUN mkdir -p /src
WORKDIR /src

ENV DOCKERIZE_VERSION v0.9.9
RUN wget https://github.com/jwilder/dockerize/releases/download/${DOCKERIZE_VERSION}/dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz -O - | tar -C /usr/local/bin -xzv

COPY src/ /src/

RUN pip install poetry==2.3.0
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi --no-root

RUN mkdir -p /src/database /src/logs

# Prepare the CMD command with the script to be run at the begining of the deploy
RUN mkdir -p /scripts
COPY docker/post_deploy.sh /scripts/post_deploy.sh

RUN useradd -m appuser && chown -R appuser:appuser /src
USER appuser

EXPOSE 8000

CMD ["sh", "/scripts/post_deploy.sh"]
