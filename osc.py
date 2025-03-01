from oscpy.client import OSCClient
import logging

class OSCManager:
    def __init__(self, host="127.0.0.1", port=8000):
        """Initialize OSC Client with given host and port."""
        self.host = host
        self.port = int(port)
        self.osc = OSCClient(self.host, self.port)
        print(f"OSC Client initialized at {self.host}:{self.port}")

    def setOSCData(self, Host, Port):
        """Updates the OSC Client with new host and port."""
        self.host = Host
        self.port = int(Port)
        self.osc = OSCClient(self.host, self.port)
        print(f"Updated OSC target: {self.host}:{self.port}")

        # Send a test message to check connectivity
        for i in range(10):
            # Always ensure '/ping' is passed as a string
            address = '/ping'
            if isinstance(address, bytes):
                address = address.decode('utf-8')  # Convert bytes to string
            self.osc.send_message(address, [i])
            print(f"Sent: {address} {i}")

    def sendOSC(self, execPage, execItem):
        """Sends an OSC message formatted for ChamSys."""
        oscstring = f"/exec/{execPage}/{execItem}"
        print(f"Sending OSC command: {oscstring}")
        self.send_message(oscstring)

    def send_message(self, address):
        """Sends an OSC message."""
        # Make sure the address is always a string before sending it
        if isinstance(address, bytes):  # If the address is in bytes, decode it
            address = address.decode('utf-8')
        
        if not isinstance(address, str):
            raise ValueError("Address must be a string.")
        
        # Send the message
        self.osc.send_message(address, [])
        print(f"Sent message to {self.host}:{self.port} -> {address}")
