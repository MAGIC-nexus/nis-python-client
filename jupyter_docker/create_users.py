import pandas as pd
import os
import sys
import crypt
import csv


def create_users(file):
    with open(file, 'r') as csvfile:
        for row in csv.reader(csvfile, delimiter=','):
            user = row[0]
            passw = row[1]
            pwd = crypt.crypt(passw, crypt.mksalt(crypt.METHOD_SHA512))
            s = "useradd -m -b /home -p '"+pwd+"' "+user
            os.system(s)


print("Creating users from file: "+sys.argv[1], flush=True)
create_users(sys.argv[1])
