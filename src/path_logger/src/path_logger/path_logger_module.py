import rospy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path

import os
import csv

class PathLogger:
    def __init__(self):
         # Set the log file path
        self.log_file_path = os.path.join(rospy.get_param('~log_file_path', '/tmp'), 'robot_path.csv')

        # Open the CSV file for writing
        self.csv_file = open(self.log_file_path, 'w')
        self.csv_writer = csv.writer(self.csv_file)

        self.robot_path_msg = Path()
        self.robot_path_pub = rospy.Publisher('/robot_path', Path, queue_size=10)
        # Write the header
        self.csv_writer.writerow(['timestamp', 'x', 'y', 'z', 'qx', 'qy', 'qz', 'qw'])

        # Subscribe to the robot's position topic
        rospy.Subscriber('/vslam2d_pose', PoseStamped, self.pose_callback)

        rospy.loginfo("PathLogger node started, logging to %s", self.log_file_path)
    
    def pose_callback(self, msg):
        # Extract position and orientation data from PoseStamped message
        timestamp = msg.header.stamp.to_sec()
        position = msg.pose.position
        orientation = msg.pose.orientation

        self.robot_path_msg.header.stamp = rospy.Time.now()
        self.robot_path_msg.header.frame_id = "map"
        self.robot_path_msg.poses.append(msg)
        self.robot_path_pub.publish(self.robot_path_msg)
        # Log the data to the CSV file
        self.csv_writer.writerow([timestamp, position.x, position.y, position.z,
                                  orientation.x, orientation.y, orientation.z, orientation.w])
    
    def shutdown(self):
        # Close the CSV file when the node is shutdown
        self.csv_file.close()