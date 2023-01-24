FROM python:3.10.9-alpine3.17
RUN adduser gitlab -D
WORKDIR /app
COPY --chown=gitlab:gitlab requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY --chown=gitlab:gitlab gitlab2github /app/gitlab2github
USER gitlab