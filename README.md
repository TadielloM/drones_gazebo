# DRONES_GAZEBO
An implementation of different collision avoidance algorithms for UAVs for Gazebo


## Requirements
Install Gazebo 9 as described in http://gazebosim.org/tutorials?tut=install_ubuntu  
Clone this project on your pc  
Export the following variable needed for Gazebo copying the following in your .bashrc  
```
source /usr/share/gazebo/setup.sh

#Gazebo variable for location of the models,worlds and plugins
export GAZEBO_RESOURCE_PATH=<PATH-TO-THE-CLONED-REPO>/drones_gazebo/worlds:${GAZEBO_RESOURCE_PATH}
export GAZEBO_MODEL_PATH=<PATH-TO-THE-CLONED-REPO>/drones_gazebo/models:${GAZEBO_MODEL_PATH}
export GAZEBO_PLUGIN_PATH=<PATH-TO-THE-CLONED-REPO>/drones_gazebo/build:${GAZEBO_PLUGIN_PATH}
```

## Usage
Install gazebo export path of model/world/plugins to .bashrc file
generetare world file wiht
```
python generate.py -n <number_of_drones> -a <algorithm> -t <test>

<algorithm>: ORCA / BAPF / EAPF
<test>: 1 / 2 
```
Run the simulation on gazebo with:
```
gazebo drones_<number of drones>.world
```

To run the same tests used in the paper:
```
chmod +x ./test.sh
./test.sh
```
Pay attention all the tests can take a couple of day of execution with this settings. Big improvement as parallelization of the execution can be done.


## To pay attention
Some of the path used for collecting data and calculate them are hard coded please change it in order to make the code working in your pc
