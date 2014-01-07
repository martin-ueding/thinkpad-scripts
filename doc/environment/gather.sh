#!/bin/bash
# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>

set -e
set -u

sudo su -c env mu | sort > env-su.txt
sudo su -c 'env env' mu | sort > env-su_env.txt
sudo env | sort > env-root.txt
env | sort > env-user.txt
