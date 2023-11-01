FROM python:3.11

SHELL ["/bin/bash", "-c"]

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8443

RUN pip install --upgrade pip

RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
 gettext cron openssh-client flake8 locales

RUN useradd -rms /bin/zsh telegram && chmod 777 /opt /run

WORKDIR /telegram
RUN mkdir /telegram/static && mkdir /telegram/media
RUN chown -R telegram:telegram /telegram && chmod 755 /telegram

COPY --chown=telegram:telegram . .

RUN pip install -r requirements.txt

USER telegram
