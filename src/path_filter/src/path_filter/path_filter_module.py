import rospy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path

import csv
import os
import math

class PathFilter:
    def __init__(self):
        rospy.init_node('path_filter')
        # self.desired_num_points = rospy.get_param('~desired_num_points', 100)
        self.desired_num_points = 100
        # Get the file path parameter
        self.csv_file_path = rospy.get_param('~csv_file_path', os.path.join(os.getcwd(), 'robot-path.csv'))

        # Open the CSV file for reading
        try:
            self.csv_file = open(self.csv_file_path, 'r')
        except IOError:
            rospy.logerr("Cannot open CSV file at %s", self.csv_file_path)
            rospy.signal_shutdown("Cannot open CSV file")

        self.csv_reader = csv.reader(self.csv_file)
        next(self.csv_reader, None)

        self.path_msg = Path()
        self.output_path_msg = Path()

        # Create a publisher for the Path data
        self.raw_path_publisher = rospy.Publisher('/raw_path', Path, queue_size=10)
        self.path_output_publisher = rospy.Publisher('/filtered_path', Path, queue_size=10)

    def set_desired_num_points(self, num):
        self.desired_num_points = num

    def read_and_publish(self):
        self.path_msg.header.frame_id = "map"

        for row in self.csv_reader:
            if rospy.is_shutdown():
                break

            if len(row) != 8:
                rospy.logwarn("Invalid row length: %s", row)
                continue

            try:
                timestamp, x, y, z, qx, qy, qz, qw = map(float, row)
            except ValueError:
                rospy.logwarn("Invalid row format: %s", row)
                continue

            pose_msg = PoseStamped()
            pose_msg.header.stamp = rospy.Time.now()
            pose_msg.header.frame_id = "map"
            pose_msg.pose.position.x = x
            pose_msg.pose.position.y = y
            pose_msg.pose.position.z = z
            pose_msg.pose.orientation.x = qx
            pose_msg.pose.orientation.y = qy
            pose_msg.pose.orientation.z = qz
            pose_msg.pose.orientation.w = qw

            self.path_msg.poses.append(pose_msg)

        rospy.loginfo("Publishing /raw_path msg")
        # Publish the complete path
        self.raw_path_publisher.publish(self.path_msg)
    
    def filter_path(self):
        filtered_path = Path()
        total_points = len(self.path_msg.poses)
        if(total_points <= self.desired_num_points):
            filtered_path.poses = self.path_msg.poses
        else:
            interval = math.floor(total_points / float(self.desired_num_points))
            print(interval)
            for i in range (self.desired_num_points):
                if i == self.desired_num_points:
                    filtered_path.poses.append(self.path_msg.poses[-1])
                    break

                index = int(i * interval)
                if(index > len(self.path_msg.poses)):
                    break
                filtered_path.poses.append(self.path_msg.poses[index])

        rospy.loginfo("Filtered path with %d points from original %d points", 
                      len(filtered_path.poses), total_points)

        for pose_stamped in filtered_path.poses:
            pose_msg = PoseStamped()
            pose_msg.header.stamp = rospy.Time.now()
            pose_msg.header.frame_id = "map"
            pose_msg.pose.position.x = pose_stamped.pose.position.x
            pose_msg.pose.position.y = pose_stamped.pose.position.y
            pose_msg.pose.position.z = pose_stamped.pose.position.z
            pose_msg.pose.orientation.x = pose_stamped.pose.orientation.x
            pose_msg.pose.orientation.y = pose_stamped.pose.orientation.y
            pose_msg.pose.orientation.z = pose_stamped.pose.orientation.z
            pose_msg.pose.orientation.w = pose_stamped.pose.orientation.w

            self.output_path_msg.poses.append(pose_msg)
        
        self.output_path_msg.header.frame_id = "map"
        self.path_output_publisher.publish(self.output_path_msg)

        
    def clear_path(self):
        self.output_path_msg = Path()
        self.output_path_msg.header.frame_id = "map"
        self.output_path_msg.header.stamp = rospy.Time.now()
        self.path_output_publisher.publish(self.output_path_msg)

    def shutdown(self):
        self.csv_file.close()
        rospy.loginfo("Path Filter node has shut down, file closed.")