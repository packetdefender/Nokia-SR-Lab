#Nokia Service Router Lab Turnup
This is a set of playbooks that automates the turn-up of 12 node vSR environment.
The key files:
KVMSetup.yml --> This is a playbook to call the KVM_SETUP role to deploy KVM and packages needed to build environment
InitalizeSREnv.yml --> Sets up Networking, creates and copies required files and setup XML files for VM deployment
Lab-Setup.yml --> Combines KVM_SETUP and SR-Lab-Init roles
DestroyEnv.yml --> Destroys and deletes all VMs, files created and all defined network bridges.  Reboots server when completed
*User needs to supply SR Image and SR License file* 
Create folder named files in the following location `~/SR-Lab-Init/` and copy qcow2 image and license file to that directory