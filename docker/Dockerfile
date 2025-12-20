FROM python:3.10.12-slim

# Install tools needed for translations
RUN apt-get update && apt-get install -y wget make gettext && apt-get clean
RUN apt-get autoclean

# Prepare work directory
RUN mkdir -p /src
WORKDIR /src

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz -O - | tar -C /usr/local/bin -xzv

COPY src/ /src/

RUN pip install poetry==1.6.1
RUN poetry config virtualenvs.create false && poetry install

RUN mkdir -p /src/database /src/logs

RUN useradd -m appuser && chown -R appuser:appuser /src
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]