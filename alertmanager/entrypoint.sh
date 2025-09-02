#!/bin/sh

sh -c "sed -e 's/MAIL_USERNAME/${MAIL_USERNAME}/g' -e 's/MAIL_PASSWORD/${MAIL_PASSWORD}/g' /etc/alertmanager/alertmanager.yml > /tmp/alertmanager.yml"

exec /bin/alertmanager --config.file=/tmp/alertmanager.yml