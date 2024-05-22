
# MovelAI Test Workspace

This is a workspace for MovelAI task, created by Nawab Aditya

## Prerequisites
- Ubuntu 22.04 x86 (Tested)
- ubuntu 20.04 x86 (Tested)

## How to install the program

Clone this repository :

```bash
  git clone https://www.github.com/nwbaditya/movelai_ws
```
Install docker:

https://docs.docker.com/desktop/install/linux-install

After the docker already installed, install the docker-compose plugin

https://docs.docker.com/compose/install/linux/

Go into the movelai_ws directory:
```bash
  cd ~/movelai_ws
```

To run the docker container :

```bash
  docker-compose up -d
```
The `docker-compose up` will build the docker image if it isn't built yet. After that, it will run the docker container.
To check the docker container if it is already running :

```bash
  docker ps
```
And then, to jump into the ros bash, you can use the shell script by running:

```bash
  bash ros_bash.sh
```
You will go into the ros bash inside the ros docker image.

## Running the program

There's 4 program that I already built, you can run it by using roslaunch.

For Robot Simulation with DWA Local Planner:

```bash
  roslaunch robot_bringup dwa_local_planner.launch
```

For Robot Simulation with Pure Pursuit Local Planner:

```bash
  roslaunch robot_bringup pure_pursuit_local_planner.launch
```

For Recording the rosbag files for robot path:

```bash
  roslaunch path_logger path_logger.launch && rosbag play bags/path_test.bag
```

For Downscaling the recorded robot path files:

```bash
  roslaunch path_filter start_path_filter_service.launch
```
Now, the path filter service will run. You can load, filter, and clear filtered data by using rosservice.

Run the following command:

Loading the data (arg1 = load, arg2 = any number):

```bash
  rosservice call /path_filter_cmd load 0
```

Filtering the data (arg1 = filter, arg2 = number of output points):
```bash
  rosservice call /path_filter_cmd filter 100
```

Clearing the filtered data (arg1 = clear, arg2 = any number):
```bash
  rosservice call /path_filter_cmd clear 0
```

## Design Documentation

I'm using navstack and turtlebot3_simulation package to build this simulation.
Below is the rqt_graph when the program is running :

![RQT Graph](https://raw.githubusercontent.com/nwbaditya/movelai_ws/main/image/rqt_graph.png)

And the rqt_tf_tree :

![RQT TF_Tree](https://raw.githubusercontent.com/nwbaditya/movelai_ws/main/image/rqt_tf_tree.png)

## Controllers

### DWA Local Planner

I choose this local planner because I think, it is such a good local planner when doing navigation task. It can
interract with the surrounding to always adjust the path it takes so it won't collide based on the costmap.

Pros :
- Much safer interacting with the environment.

Cons:
- Quite heavy in computation because it will always calculating the window near the robot.
- Quite complex algorithm to understand.

For the DWA Local Planner, it is a plugin from ros navstack. And how to tune the parameters, it can be found here:

https://wiki.ros.org/dwa_local_planner

You can found the tuning parameters here:

```bash
  movelai_ws/src/robot_bringup/params/dwa_local_planner_params_waffle_pi.yaml
```
![DWA Local Planner Params](https://raw.githubusercontent.com/nwbaditya/movelai_ws/main/image/dwa_planner_params.png)

### Pure Pursuit Planner

I choose this pure pursuit planner because it is the simplest path following algorithm that I can found and built. I built this navstack plugins myself,
and it can integrate with the move_base package from navstack.

Pros :
- Quite light in terms of computing.
- Simple to tune and understands.

Cons:
- Needs adjustment in algorithm when interracting with environment, because it doesnt care about everything near the robot.
- Not accurately in terms of heading goal.

You can found the tuning parameters here:

```bash
  movelai_ws/src/robot_bringup/params/pure_pursuit_planner_params_waffle_pi.yaml
```
![Pure_Pursuit Planner Params](https://raw.githubusercontent.com/nwbaditya/movelai_ws/main/image/pure_pursuit_planner_params.png)

How to tune:
- position_accuracy : the radius of robot that already counted as a success reaching the goal
- kp_linear : Proportional gain of the linear velocity
- kp_angular : Proportional gain of the angular velocity

Reference : https://thomasfermi.github.io/Algorithms-for-Automated-Driving/Control/PurePursuit.html

### Running The Simple Waypoints Generator

```bash
  rosrun simple_waypoints simple_waypoints.py
```

## Downscaling Robot Path
For the downscaling the path algorithm, I'm just use simple sampling based on how much output points. For example, if I want to output 10 points from
1000 raw points, then I could divide the sampling intervals to 100 points. But remember, the most critical path is the starting and the goal. I should always
taking the start point and the goal point, so I won't miss the path alot. There's some case if the interval is not integer, so it will end up in a point which
is maybe not the goal path.

## Running the unit test

To run the unit test on path_filter module, run the following command:

```bash
rostest path_filter test_path_filter_service.py
```


## My Journey about how to solve the task

At first, I little bit surprised on how tight the timeline to solve the task. One week creating robot simulation with at least two controllers implemented.

So, to overcome that problems, I choose to use open source github repo from another people who already built the sim environment, combine it with turtlebot3 stack.

Okay, one problem already solved, but there's another problem, creating the controllers. I choose to use navstack from ROS, that already built in package such as move_base, 
amcl, and map_server along with rviz configuration. With that, I could do localization, path planning, and path following. For the localization, I am using AMCL localization as 
I ever use it on the real mobile robots when I'm in college. And for the path planning, I use the default global path planner from navstack, navfn as it always adjust with the 
environment when the robot move, so it won't collide with the walls. Actually, I ever use A* on my robots when in college, but there's some problem with it as it takes the shortest 
route based on the costmap, and always taking the route the shortest distance to the wall. It will be disaster if I combine it with the classic pure pursuit algorithm as if it only look 
ahead where the next waypoint located without knowing what is near the robot.

## Authors

- [@nwbaditya](https://www.github.com/nwbaditya)

