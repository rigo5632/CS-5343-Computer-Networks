# Sofware Defined Networks

## Programming Mininet Topologies

In the topo directory, there are a variety of python files each defining a topology. 
Executing the python script will result in a CLI where you can execute mininet commands for the defined topology.

Install Necessary Packages (Ubuntu):

*sudo apt install mininet*

*sudo apt-get install openvswitch-testcontroller*

Executing the Script:

*sudo cp /usr/bin/ovs-testcontroller /usr/bin/ovs-controller*

*sudo python topos/part1.py*


## SDN Controller using POX

Under the pox directory, we used a skeleton POX controller and modified it to create a firewall that allows all ARP and ICMP traffic to pass.

Install Necessary Package:

*git clone http://github.com/noxrepo/pox*

In order for the controller to function, run the following commands concurrently:

*/pox.py part2controller* #run first (the *pox.py* file should be found under the default branch folder)

*sudo ./part2* #run second



