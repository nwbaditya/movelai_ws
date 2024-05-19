#!/usr/bin/env python

import rospy
import rostest
import unittest
from path_filter.srv import PathFilterCmd

class TestPathFilterService(unittest.TestCase):
    def test_load_path(self):
        # Wait for the service to become available
        rospy.wait_for_service('path_filter_cmd')

        try:
            # Create a service proxy
            path_filter_cmd = rospy.ServiceProxy('path_filter_cmd', PathFilterCmd)
            
            # Call the 'load' command
            response = path_filter_cmd("load")

            # Check if the response indicates success
            self.assertEqual(response.result, "Loading Path Success.")

        except rospy.ServiceException as e:
            self.fail("Service call failed: %s" % e)

    def test_filter_path(self):
        # Wait for the service to become available
        rospy.wait_for_service('path_filter_cmd')

        try:
            # Create a service proxy
            path_filter_cmd = rospy.ServiceProxy('path_filter_cmd', PathFilterCmd)
            
            # Call the 'filter' command
            response = path_filter_cmd("filter")

            # Check if the response indicates success
            self.assertEqual(response.result, "Filtering Path Success.")

        except rospy.ServiceException as e:
            self.fail("Service call failed: %s" % e)

    def test_clear_path(self):
        # Wait for the service to become available
        rospy.wait_for_service('path_filter_cmd')

        try:
            # Create a service proxy
            path_filter_cmd = rospy.ServiceProxy('path_filter_cmd', PathFilterCmd)
            
            # Call the 'clear' command
            response = path_filter_cmd("clear")

            # Check if the response indicates success
            self.assertEqual(response.result, "Path Cleared.")

        except rospy.ServiceException as e:
            self.fail("Service call failed: %s" % e)

if __name__ == "__main__":
    rostest.rosrun('path_filter', 'test_path_filter_service', TestPathFilterService)
