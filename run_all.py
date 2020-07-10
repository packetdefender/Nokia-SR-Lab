#!/usr/bin/python3
###########################################
#                                         #
#       UUID Generator for SR-Lab         #
#       BoF Generator for SR-Lab          #
#       Variable Change for SR-Lab        #
#                                         #
#       v1.4 Author: Mike Lossmann        #
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
        uuid_lst = []
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
                # print(f'R{n} has a UUID of: {uuid_rt}')
                uuid_lst.append(str(uuid_rt))
            return uuid_lst
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


def bof_address_assign(num_rtr):
    while True:
        num_rtr_lst = list(range(1, num_rtr+1))
        try:
            ip = ipaddress.ip_network(
                input("What is the IP address range you are looking for: "))
            ip_range = list(ip.hosts())
            available_ips = []
            for i in ip_range:
                print(f'Currently Pinging {i}')
                ret = os.system(f'ping -o -c 2 -W 3000 {i} >> /dev/null')
                if ret != 0:
                    a_ip = str(i)
                    available_ips.append(a_ip)
            if len(available_ips) < num_rtr_lst[-1]:
                print('You do not have enough IP addresses for your topology')
                continue
            default_gateway = available_ips[-1].split('.')
            default_gateway[-1] = '1'
            dg = ".".join(default_gateway)
            for rtr in num_rtr_lst:
                with open(f'{hv_path}/R{rtr}.yml') as f:
                    yml_doc = yaml.load(f)
                    if 'vsr_mgmt' in yml_doc:
                        yml_doc['vsr_mgmt'] = available_ips[rtr-1]
                        yml_doc['vsr_mgmt_gw'] = dg
                with open(f'{hv_path}/R{rtr}.yml', "w") as f:
                    yaml.dump(yml_doc, f)

            bof_ipdict = {'R'+str(num_rtr_lst[i]): [available_ips[i]]
                          for i in range(len(num_rtr_lst))}
            bof_ipdict['gateway'] = dg
            return bof_ipdict

        except ValueError:
            print('Please only enter an IP address in dotted decimal format')


def data_manipulation(rtr_uuid, bof_addr):
    gw = bof_addr.pop('gateway')
    for k, v in bof_addr.items():
        bof_addr[k].append(rtr_uuid.pop(0))
    return bof_addr, gw


def printer(dm, gateway):
    print('-'*91)
    print('''Your lab variables have been set and are printed below.  
    Please request a vSIM license for the below UUIDs, 
    before running Ansible Playbooks''')
    print('-'*91)
    print(f'{"Router":^10} | {"UUID":^40} | {"IP Address":^15} | {"Default Gateway":^15} |')
    print('-'*91)
    for rtr, lst in dm.items():
        print(f'{rtr:^10} | {lst[1]:^40} | {lst[0]:^15} | {gateway:^15} |')
    print('-'*91)


rtr_uuid = uuid_gen(no_of_rtr)
change_remote_user_target_host(ru, ts)
bof = bof_address_assign(no_of_rtr)
bof_uuid, gw = data_manipulation(rtr_uuid, bof)
printer(bof_uuid, gw)
