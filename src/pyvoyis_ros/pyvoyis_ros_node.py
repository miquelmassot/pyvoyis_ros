#!/usr/bin/env python
# -*- coding: utf-8 -*-


import rospy
from std_srvs.srv import Empty
import xmlrpclib
import time
import socket


class VoyisROS:
    def __init__(self):
        rospy.init_node("pyvoyis_ros_node", log_level=rospy.INFO)

        # Get parameters
        configuration_file = rospy.get_param(
            "~configuration_file")
        
        time.sleep(5)
        print("Trying to connect to http://localhost:8000")

        self.xmlrpc_server = xmlrpclib.ServerProxy('http://localhost:8000')    
        print("Trying to call RUN...")
        while True:
            try:    
                self.xmlrpc_server.run(configuration_file)
                time.sleep(1)
            except socket.error, exc:
                print "Caught exception socket.error : %s" % exc    
            break
        

        # Offer start_acquisition service
        rospy.Service("~start_acquisition", Empty, self.start_acquisition_srv_cb)
        # Offer stop_acquisition service
        rospy.Service("~stop_acquisition", Empty, self.stop_acquisition_srv_cb)

        print("Ready")
        # Spin as a single-threaded node
        r = rospy.Rate(1)
        while not rospy.is_shutdown():
            r.sleep()
        self.xmlrpc_server.kill()


    def start_acquisition_srv_cb(self, req):
        self.xmlrpc_server.start_acquisition()

    def stop_acquisition_srv_cb(self, req):
        self.xmlrpc_server.stop_acquisition()


if __name__ == '__main__':
    vr = VoyisROS()