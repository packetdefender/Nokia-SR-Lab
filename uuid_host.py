#!/usr/bin/python3
###########################################
#                                         #
#       UUID Generator for SR-Lab         #
#       BoF Generator for SR-Lab          #
#       Variable Change for SR-Lab        #
#                                         #
#       v1.0 Author: Mike Lossmann        #
#                                         #
###########################################
import uuid
import sys
from ruamel.yaml import YAML
import os
import re
import ipaddress

yaml = YAML()
yaml.indent(mapping=4, sequence=4, offset=2)
pwd = os.getcwd()
hv_path = f'{pwd}/host_vars/'
gv_path = f'{pwd}/group_vars/'


def uuid_gen():
    while True:
        try:
            num_rtr = int(input('How many routers are you deploying: '))
            if num_rtr == 0:
                print('Zero is not a valid input')
                break
            elif num_rtr > 12:
                print("Script will only generate up to 12 UUIDs")
                continue
            for n in range(1, num_rtr+1):
                rtr = str(n)
                uuid_rt = uuid.uuid4()
                with open(f'{hv_path}/R{rtr}.yml') as f:
                    yml_doc = yaml.load(f)
                    if 'uuid' in yml_doc:
                        yml_doc['uuid'] = str(uuid_rt)
                with open(f'{hv_path}/R{rtr}.yml', "w") as f:
                    yaml.dump(yml_doc, f)

                print(f'R{n} has a UUID of: {uuid_rt}')
            break
        except ValueError:
            print("Please only enter Numbers from 1-12.")


def change_remote_user_target_host():
    remote_user = input("Please enter the target server's username: ")
    while True:
        target_server = input("Please enter the target server's IP Address: ")
        ip_regex = re.compile(
            r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
        is_ip = ip_regex.fullmatch(target_server)
        if is_ip == None:
            print(f"{target_server} is not a valid IP Address")
            continue
        for file in os.listdir(gv_path):
            file_name = gv_path+file
            with open(file_name) as f:
                yml_doc = yaml.load(f)
                if 'remote_user' and 'target_server' in yml_doc:
                    yml_doc['remote_user'] = str(remote_user)
                    yml_doc['target_server'] = target_server
            with open(file_name, "w") as f:
                yaml.dump(yml_doc, f)
        break


uuid_gen()
change_remote_user_target_host()
