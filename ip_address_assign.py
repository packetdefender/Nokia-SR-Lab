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

print('*' * 35)
print('''
This script will generate BoF addresses and modify each router's
host_vars yml file for you based on the IP range that is input
into the script.  The script assumes the default gateway is
ends in .1
''')
print('*' * 35)
input_rtr = int(input('How many routers are you deploying: '))


def bof_address_assign(ir):
    num_rtr_lst = list(range(1, ir + 1))
    while True:
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

            r_ipdict = {'R'+str(num_rtr_lst[i]): available_ips[i]
                        for i in range(len(num_rtr_lst))}

            return r_ipdict, dg
        except ValueError:
            print('Please only enter an IP address in dotted decimal format')
        except TypeError:
            print('Please only enter a number from 1 - 12')


def printer(dm, gateway):
    print('-'*52)
    print('''Your lab variables have been set and printed below.
    ''')
    print('-'*52)
    print(f'{"Router":^10}  {"IP Address":^15} | {"Default Gateway":^15} |')
    print('-'*52)
    for rtr, lst in dm.items():
        print(f'{rtr:^10} | {lst:^15} | {gateway:^14} |')
    print('-'*52)


bof, gw = bof_address_assign(input_rtr)
printer(bof, gw)
