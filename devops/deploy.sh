#!/bin/bash

set -e

git pull origin main

sudo cp devops/podcaster.service /etc/systemd/system/podcaster.service

sudo systemctl daemon-reload

sudo systemctl restart podcaster.service
