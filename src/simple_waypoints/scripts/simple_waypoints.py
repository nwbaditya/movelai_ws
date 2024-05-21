#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseActionResult

class WaypointPublisher:
    def __init__(self):
        rospy.init_node('simple_waypoints', anonymous=True)
        self.pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
        self.sub = rospy.Subscriber('/move_base/result', MoveBaseActionResult, self.result_callback)
        self.waypoints = [
            (0.09260620921850204, 3.4109835624694824, 0.0, 0.0, 0.0, 0.3933981472565199, 0.3933981472565199),
            (2.8559093475341797, -0.3686366081237793, 0.0, 0.0, 0.0, -0.026288734454521515, 0.9996543914977715),
            (5.726131439208984, 2.2379748821258545, 0.0, 0.0, 0.0, 0.7071067966408575, 0.7071067966408575),
            (3.2990918159484863, 3.199544906616211, 0.0, 0.0, 0.0, -0.07625090820138845, 0.9970886615534565),
            (3.8331820964813232, 0.06318134069442749, 0.0, 0.0, 0.0, -0.9808826424576396, 0.19460020998271946)
            ]
              # Example waypoint 1        ]
        self.current_waypoint_index = 0
        self.reached_goal = True

        while self.pub.get_num_connections() == 0:
            rospy.loginfo("Waiting for subscribers...")
            rospy.sleep(1)

    rospy.loginfo("Publisher initialized and connected to subscribers.")

    def result_callback(self, msg):
        if msg.status.status == 3:  # Goal reached
            self.reached_goal = True

    def publish_next_waypoint(self):
        if self.current_waypoint_index < len(self.waypoints):
            pose = PoseStamped()
            pose.header.frame_id = "map"  # Adjust frame ID if needed
            pose.header.stamp = rospy.Time.now()
            waypoint = self.waypoints[self.current_waypoint_index]
            pose.pose.position.x = waypoint[0]
            pose.pose.position.y = waypoint[1]
            pose.pose.position.z = waypoint[2]
            pose.pose.orientation.x = waypoint[3]
            pose.pose.orientation.y = waypoint[4]
            pose.pose.orientation.z = waypoint[5]
            pose.pose.orientation.w = waypoint[6]  # Assuming no rotation
            self.pub.publish(pose)
            self.reached_goal = False
            self.current_waypoint_index += 1
            rospy.loginfo("Publishing waypoints at [%f, %f]", waypoint[0], waypoint[1])
        
        else:
            rospy.signal_shutdown("All waypoints already published.")

    def run(self):
        rate = rospy.Rate(1)  # Adjust the rate as needed
        while not rospy.is_shutdown():
            # rospy.loginfo("simple_waypoints_node is running...")
            if self.reached_goal:
                self.publish_next_waypoint()
            rate.sleep()

if __name__ == '__main__':
    wp_publisher = WaypointPublisher()
    wp_publisher.run()
