# Nokia Service Router Lab Turnup

[![Build Status](https://travis-ci.org/mlossmann/Nokia-SR-Lab.svg?branch=master)](https://travis-ci.org/mlossmann/Nokia-SR-Lab)

This is a set of playbooks that automates the turn-up of 12 node vSR environment.

```
The key files:
KVMSetup.yml --> This is a playbook to call the KVM_SETUP role to deploy KVM and packages needed to build environment
InitalizeSREnv.yml --> Sets up Networking, creates and copies required files and setup XML files for VM deployment
Lab-Setup.yml --> Combines KVM_SETUP and SR-Lab-Init roles
DestroyEnv.yml --> Destroys and deletes all VMs, files created and all defined network bridges.  Reboots server when completed
```

*User needs to supply SR Image and SR License file*. 

Create folder named files in the following location `~/SR-Lab-Init/` and copy qcow2 image and license file to that directory so scripts can copy files accordingly

In `~/group_vars/` directory there are two files where the ansible orchestration username is hardcoded as well as the target server.  Changes should be done at the following locations:

```
> all.yml
>>target_server_username
>>target_server should be changed to the server you targeted for this script to run on
----
> KVMHosts.yml
>>ansible_ssh_user
```

In `~/group_vars/SRHosts.yml` the variable `remote_user` should also be changed to your ansible orchestration username.  There are tasks that will pull this variable in when creating folders and copying information.

in `~/host_vars/` each router has their BoF address defined with the gateway {vsr_mgmt} and {vsr_mgmt_gw}. Be sure to modify those fields for your specific BoF configuration
