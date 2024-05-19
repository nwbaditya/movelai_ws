#!/usr/bin/env python

import rospy
from path_filter.srv import PathFilterCmd, PathFilterCmdResponse
from path_filter.path_filter_module import PathFilter


path_filter = PathFilter()

def path_filter_cb(req):
    if req.cmd == "load":
        path_filter.read_and_publish()
        return PathFilterCmdResponse("Loading Path Success.")
    elif req.cmd == "filter":
        path_filter.filter_path()
        return PathFilterCmdResponse("Filtering Path Success.")
    elif req.cmd == "clear":
        path_filter.clear_path()
        return PathFilterCmdResponse("Path Cleared.")

if __name__ == "__main__":
    service = rospy.Service('path_filter_cmd', PathFilterCmd, path_filter_cb)
    rospy.loginfo("Path Filter Server is running.")
    rospy.spin()