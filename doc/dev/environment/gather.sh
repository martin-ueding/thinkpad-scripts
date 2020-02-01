#!/bin/bash
# Copyright © 2014 Martin Ueding <martin-ueding.de>

env | sort > env-user.txt
sudo env | sort > env-root.txt
sudo su -c env mu | sort > env-su.txt
sudo su -c 'env env' mu | sort > env-su_env.txt

diff -u env-user.txt env-root.txt > diff-user-root.diff
diff -u env-user.txt env-su.txt > diff-user-su.diff
diff -u env-user.txt env-su_env.txt > diff-user-su_env.diff
