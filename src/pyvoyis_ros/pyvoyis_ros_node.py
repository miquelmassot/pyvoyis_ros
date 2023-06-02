#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import rospy
import rospkg
from pathlib import Path
from std_srvs.srv import Empty

from pyvoyis import Configuration, VoyisAPI


class VoyisROS:
    def __init__(self):
        rospy.init_node("pyvoyis_ros_node", log_level=rospy.INFO)

        rospack = rospkg.RosPack()

        try:
            package_path = rospack.get_path("pyvoyis_ros")
        except rospkg.ResourceNotFound:
            rospy.logerr("pyvoyis_ros package not found")
            return

        default_configuration_file = Path(package_path) / "configuration.yaml"

        if not default_configuration_file.is_file():
            rospy.logerr("Default configuration file not found")
            rospy.logerr("Please create a configuration file in {}".format(default_configuration_file))
            return

        # Get parameters
        configuration_file = rospy.get_param(
            "~configuration_file",
            str(default_configuration_file))

        self.config = Configuration(configuration_file)
        self.api = VoyisAPI(self.config)

        # Offer start_acquisition service
        rospy.Service("~start_acquisition", Empty, self.start_acquisition_srv_cb)
        # Offer stop_acquisition service
        rospy.Service("~stop_acquisition", Empty, self.stop_acquisition_srv_cb)

        self.api.run()

        # Spin as a single-threaded node
        rospy.spin()

    def start_acquisition_srv_cb(self, req):
        self.api.request_acquisition()
        return True

    def stop_acquisition_srv_cb(self, req):
        self.api.request_stop()
        return True


if __name__ == '__main__':
    vr = VoyisROS()