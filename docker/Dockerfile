# ROS distribution to use
ARG ROS_DISTRO=noetic

########################################
# Base Image                           #
########################################

FROM osrf/ros:${ROS_DISTRO}-desktop as base

ENV ROS_DISTRO=${ROS_DISTRO}
SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get install -y git
RUN apt install ros-${ROS_DISTRO}-gazebo-ros-pkgs -y
# RUN apt-get install libsdl-image1.2-dev -y
# RUN apt-get install libsdl-dev

###########################################
# Overlay Image for TurtleBot3 Simulation #
###########################################
# FROM base AS overlay
 
RUN apt-get install python3-catkin-tools -y

# Create an overlay Catkin workspace
RUN mkdir -p /movelai_ws/src
# WORKDIR /movelai_ws
# COPY ./src /src

RUN source /opt/ros/${ROS_DISTRO}/setup.bash \
 && cd /movelai_ws/src \ 
 && catkin_init_workspace

COPY ./src /movelai_ws/src
COPY ./bags /movelai_ws/bags

WORKDIR /movelai_ws

RUN source /opt/ros/${ROS_DISTRO}/setup.bash \
 && sudo rosdep fix-permissions \
 && rosdep update \
 && rosdep install --from-paths src -y --ignore-src \
 && catkin_make

RUN source /movelai_ws/devel/setup.bash
ENV TURTLEBOT3_MODEL = waffle_pi

# Set up the work directory and entrypoint
WORKDIR /movelai_ws
 
# Set up the entrypoint
COPY ./docker/entrypoint.sh /
ENTRYPOINT [ "/entrypoint.sh" ]

#####################
# Development Image #
#####################
# FROM overlay as dev
 
# Dev container arguments
ARG USERNAME=devuser
ARG UID=1000
ARG GID=${UID}
 
# Install extra tools for development
RUN apt-get update && apt-get install -y --no-install-recommends \
 gdb gdbserver nano
 
# Create new user and home directory
RUN groupadd --gid $GID $USERNAME \
 && useradd --uid $UID --gid $GID --create-home $USERNAME \
 && echo "$USERNAME ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME \
 && chmod 0440 /etc/sudoers.d/$USERNAME \
 && mkdir -p /home/$USERNAME \
 && chown -R $UID:$GID /home/$USERNAME
 
# Set the ownership of the overlay workspace to the new user
RUN chown -R ${UID}:${GID} /movelai_ws/ 
 
# Set the user and source entrypoint in the user's .bashrc file
USER ${USERNAME}
RUN echo "source /entrypoint.sh" >> /home/${USERNAME}/.bashrc
