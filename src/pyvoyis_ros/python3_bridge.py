from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from pyvoyis import Configuration, VoyisAPI

import threading
import time


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/RPC2",)


class PyVoyisXMLRPCServer:
    def __init__(self):
        # Create server
        self.server = SimpleXMLRPCServer(
            ("localhost", 8000), requestHandler=RequestHandler, allow_none=True
        )

        self.api = None
        self.asked_to_run = False
        self.asked_to_acquire = False
        self.time_since_request_s = 0
        self.timeout_s = 60

        self.run_thread = threading.Thread(target=self.api_thread)
        self.run_thread.start()
        self.safety_thread = threading.Thread(target=self.safety_thread)
        self.safety_thread.start()

        self.server.register_function(self.run)
        self.server.register_function(self.kill)

        # Run the server's main loop
        print("Serving forever...")
        self.server.serve_forever()

    def api_thread(self):
        while not self.asked_to_run:
            print("sleeping thread...")
            time.sleep(5)
        print("Called to RUN!")
        self.api = VoyisAPI(self.config)
        self.api.run()

    def safety_thread(self):
        try:
            while True:
                if not self.asked_to_acquire:
                    continue

                self.time_since_request_s += 1

                if self.time_since_request_s < self.timeout_s:
                    continue

                if self.api.state.is_acquiring:
                    continue

                print("Safety timeout reached, restarting Voyis API")
                self.api.shutdown()
                self.api = VoyisAPI(self.config)
                self.api.run()
                print("Restarted Voyis API, requesting acquisition...")
                self.api.request_acquisition()
                self.time_since_request_s = 0
                time.sleep(1)
        except KeyboardInterrupt:
            pass

    def run(self, configuration_file):
        # Called by pyvoyis_ros_node.py at initialization
        self.config = Configuration(configuration_file)
        self.server.register_function(self.start_acquisition)
        self.server.register_function(self.stop_acquisition)
        self.asked_to_run = True
        return True

    def kill(self):
        # Called by pyvoyis_ros_node.py at ROS shutdown
        if self.api:
            self.api.shutdown()

    def start_acquisition(self):
        # Called by pyvoyis_ros_node.py when start_acquisition service is called
        print("start_acquisition called")
        self.time_since_request_s = 0
        self.asked_to_acquire = True
        self.api.request_acquisition()
        return True

    def stop_acquisition(self):
        # Called by pyvoyis_ros_node.py when stop_acquisition service is called
        print("stop_acquisition called")
        self.asked_to_acquire = False
        self.api.request_stop()
        return True


if __name__ == "__main__":
    server = PyVoyisXMLRPCServer()
