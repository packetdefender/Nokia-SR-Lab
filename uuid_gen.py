#!/usr/bin/python3
###########################################
#       UUID Generator for SR-Lab         #
#                                         #
#       v1.0 Author: Mike Lossmann        #
#                                         #
###########################################
import uuid
import sys
from ruamel.yaml import YAML
import os


yaml = YAML()
yaml.indent(mapping=4, sequence=4, offset=2)
yaml.preserve_quotes = True
pwd = os.getcwd()
work_path = f'{pwd}/host_vars/'
while True:
    try:
        num_rtr = int(input('How many routers are you deploying: '))
        if num_rtr == 0:
            print('Zero is not a valid input, please enter a number from 1 - 12')
            continue
        elif num_rtr > 12:
            print("Script will only generate up to 12 UUIDs, please enter a number from 1 - 12")
            continue
        for n in range(1, num_rtr+1):
            rtr = str(n)
            uuid_rt = uuid.uuid4()
            with open(f'{work_path}/R{rtr}.yml') as f:
                yml_doc = yaml.load(f)
            # for k,v in yml_doc.items():
                # if yml_doc['uuid']:
                yml_doc['uuid'] = str(uuid_rt)
            with open(f'{work_path}/R{rtr}.yml', "w") as f:
                yaml.dump(yml_doc, f)

            print(f'R{n} has a UUID of: {uuid_rt}')
        break
    except ValueError as err:
        print("Please only enter a numbers from 1 - 12.")
