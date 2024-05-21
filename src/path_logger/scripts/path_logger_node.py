#!/usr/bin/env python

import rospy
from path_logger.path_logger_module import PathLogger

if __name__ == '__main__':
    rospy.init_node('path_logger', anonymous=True)
    path_logger = PathLogger()

    rospy.on_shutdown(path_logger.shutdown)

    rospy.spin()