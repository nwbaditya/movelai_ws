#!/bin/bash
 
# Source ROS and Catkin workspaces
source /opt/ros/noetic/setup.bash
if [ -f /turtlebot3_ws/devel/setup.bash ]
then
  source /turtlebot3_ws/devel/setup.bash
fi
if [ -f /movelai_ws/devel/setup.bash ]
then
  source /movelai_ws/devel/setup.bash
fi
echo "Sourced Catkin workspace!"
 
# Set environment variables
export TURTLEBOT3_MODEL=waffle_pi
 
# Execute the command passed into this entrypoint
exec "$@"