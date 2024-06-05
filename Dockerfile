FROM python:3.12.3-alpine3.19
LABEL maintainer pawan

RUN apk update \
    && apk add --no-cache bash make build-base jq  busybox-suid

RUN addgroup -S app && adduser -S app -G app -h /app \
    && mkdir -p /app
# RUN pip install --no-cache-dir -r test-requirements.txt
RUN python -m pip --no-cache-dir install shutils imaplib2 requests mysql-connector-python httplib2 snowflake-connector-python

WORKDIR /app
COPY . /app
ADD cron/reporting-cron.txt /app/
RUN /usr/bin/crontab /app/reporting-cron.txt \
    && /usr/bin/crontab -l

VOLUME /var/log

CMD ["crond","-f", "-l", "2"]