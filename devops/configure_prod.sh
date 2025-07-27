#!/bin/bash

set -e

cp devops/podcaster.franciszekk.conf
cp devops/podcaster.service /etc/systemd/system/podcaster.service

nginx -t
service nginx restart

systemctl daemon-reload
systemctl restart podcaster.service
