#!/usr/bin/env bash

python3 /root/create_users.py /root/users.csv
jupyterhub -f /root/jupyterhub_config.py
#jupyter labhub