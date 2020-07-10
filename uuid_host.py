#!/usr/bin/python3
###########################################
#                                         #
#      UUID Generator + Host Config       #
#                                         #
#       v1.4 Author: Mike Lossmann        #
#                                         #
###########################################
import uuid
import sys
from ruamel.yaml import YAML
import os
import re

yaml = YAML()
yaml.indent(mapping=4, sequence=4, offset=2)
pwd = os.getcwd()
hv_path = f'{pwd}/host_vars/'
gv_path = f'{pwd}/group_vars/'

while True:
    no_of_rtr = int(input('How many routers are you deploying: '))
    if no_of_rtr == 0:
        print('Zero is not a valid input')
        continue
    elif no_of_rtr > 12:
        print("Script will only generate up to 12 UUIDs")
        continue
    ru = input("Please enter the target server's username: ")
    break

while True:
    ts = input("Please enter the target server's IP address: ")
    ip_regex = re.compile(
        r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
    is_ip = ip_regex.fullmatch(ts)
    if is_ip == None:
        print(f"{ts} is not a valid IP Address")
        continue
    else:
        print(
            f'You are generating configuration for {no_of_rtr} with the target server: {ts} and a remote user of: {ru}')
        break


def uuid_gen(num_rtr):
    while True:
        rtr_uuid = {}
        num_rtr_lst = list(range(1, num_rtr+1))
        try:
            for n in range(1, num_rtr+1):
                rtr = str(n)
                uuid_rt = uuid.uuid4()
                with open(f'{hv_path}/R{rtr}.yml') as f:
                    yml_doc = yaml.load(f)
                    if 'uuid' in yml_doc:
                        yml_doc['uuid'] = str(uuid_rt)
                with open(f'{hv_path}/R{rtr}.yml', "w") as f:
                    yaml.dump(yml_doc, f)
                # uuid_lst.append(str(uuid_rt))
                rtr_uuid['R'+str(n)] = str(uuid_rt)
            return rtr_uuid
        except ValueError:
            print("Please only enter Numbers from 1-12.")


def change_remote_user_target_host(remote_user, target_server):
    while True:
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


def printer(dm):
    print('-'*55)
    print('''Your lab variables have been set and are printed below.
    Please request a vSIM license for the below UUIDs,
    before running Ansible Playbooks''')
    print('-'*55)
    print(f'{"Router":^10} | {"UUID":^40} | ')
    print('-'*55)
    for rtr, lst in dm.items():
        print(f'{rtr:^10} | {lst:^40} | ')
    print('-'*55)


rtr_uuid = uuid_gen(no_of_rtr)
change_remote_user_target_host(ru, ts)
# print(rtr_uuid)
printer(rtr_uuid)
