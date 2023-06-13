from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from pyvoyis import Configuration, VoyisAPI

import threading
import time

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

class PyVoyisXMLRPCServer:
    def __init__(self):
        # Create server
        self.server = SimpleXMLRPCServer((
            "localhost", 8000),
            requestHandler=RequestHandler,
            allow_none=True)
        
        self.api = None
        self.asked_to_run = False

        self.run_thread = threading.Thread(target=self.api_thread)
        self.run_thread.start()

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
        self.api.sync_time_manually()
        self.api.run()

    def run(self, configuration_file):
        print("RUN called")
        self.config = Configuration(configuration_file)
        self.server.register_function(self.start_acquisition)
        self.server.register_function(self.stop_acquisition)
        self.asked_to_run = True
        return True
    
    def kill(self):
        if self.api:
            self.api.shutdown()

    def start_acquisition(self):
        print("start_acquisition called")
        self.api.request_acquisition()
        return True

    def stop_acquisition(self):
        print("stop_acquisition called")
        self.api.request_stop()
        return True

if __name__ == "__main__":
    server = PyVoyisXMLRPCServer()   