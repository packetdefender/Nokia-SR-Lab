# Nokia Service Router Lab Turnup

Travis CI Build Status:[![Build Status](https://travis-ci.org/mlossmann/Nokia-SR-Lab.svg?branch=master)](https://travis-ci.org/mlossmann/Nokia-SR-Lab)

This is a set of playbooks that automates the turn-up of 12 node vSR environment.

```bash
The key files:
KVMSetup.yml --> This is a playbook to call the KVM_SETUP role to deploy KVM and packages needed to build environment
InitalizeSREnv.yml --> Sets up Networking, creates and copies required files and setup XML files for VM deployment
Lab-Setup.yml --> Combines KVM_SETUP and SR-Lab-Init roles
DestroyEnv.yml --> Destroys and deletes all VMs, files created and all defined network bridges.  Reboots server when completed
```

*User needs to supply SR Image and SR License file*.

Create folder named files in the following location `~/SR-Lab-Init/` and copy qcow2 image and license file to that directory so scripts can copy files accordingly

Before running InitalizeSREnv.yml playbook, there are three Python scripts you can choose to run that are located in the project root directory:

```bash
uuid_gen.py --> This will randomly generate n number of UUIDs for the vSRs that are going to be instanciated.
uuid_host.py --> This will randomly generate n number of UUIDs for the vSRs that are going to be instanciated as well as ask the user what the target host is and the ansible username they are using is
ip_address_assign.py --> This will prompt the user for an IP range where they want to pull management IP adddresses from and will test to see if the address is alive.  If address is free it will modify the routers host_vars file with the address.
run_all.py --> Runs all the scripts from above and returns relevent information
```

If you choose to NOT run the initlization scripts, the files can be manually edited in the following locations:

In `~/group_vars/` directory there are two files where the ansible orchestration username is hardcoded as well as the target server.  Changes should be done at the following locations:

```bash
> all.yml
>>remote_user > Change to your ansible user account
>>target_server > should be changed to the server you are targeting this script to run on
----
> KVMHosts.yml
>>ansible_ssh_user > Change to your ansible user account
```

In `~/host_vars/` each router has their BoF address defined with the gateway {vsr_mgmt} and {vsr_mgmt_gw}. Be sure to modify those fields for your specific BoF configuration.  Also each router has its interface configuration laid out in the following list:

```bash
uuid:
phy_interfaces:
    - int_name:
      ip_addr:
      port:
loopbacks:
    - loop_name:
      ip_addr:
sys_ip:
    - ip_addr:
```

If you would like to modify any part of the interface configuration, please edit the individual router host_var files.
