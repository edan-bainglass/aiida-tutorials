#!/usr/bin/env bash

sudo service postgresql stop
sudo service rabbitmq-server stop

verdi daemon stop
