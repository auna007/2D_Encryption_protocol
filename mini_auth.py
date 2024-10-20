from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.topo import Topo
import requests

class CustomTopo(Topo):
    def build(self):
        # Define hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        
        # Define switches with OpenFlow13 protocol
        s1 = self.addSwitch('s1', protocols='OpenFlow13')
        s2 = self.addSwitch('s2', protocols='OpenFlow13')
        s3 = self.addSwitch('s3', protocols='OpenFlow13')
        
        # Add links between hosts and switches
        self.addLink(h1, s1)  # h1 connected to s1
        self.addLink(h2, s2)  # h2 connected to s2
        self.addLink(h3, s3)  # h3 connected to s3
        
        # Interconnect the switches to create a network path
        self.addLink(s1, s2)  # s1 connected to s2
        self.addLink(s2, s3)  # s2 connected to s3
        self.addLink(s1, s3)  # Optionally, connect s1 directly to s3

def authenticate_user(auth_url):
    """Authenticate user using a given authentication URL."""
    while True:
        # Collect user credentials
        username = input("Enter username: ")
        password = input("Enter password: ")
        totp_code = input("Enter TOTP code: ")

        # Prepare authentication data
        data = {
            "username": username,
            "password": password,
            "totp_code": totp_code
        }

        # Send authentication request
        response = requests.post(auth_url, json=data)
        print(response.content.decode())  # Decode response content to string

        # Check if authentication was successful
        if response.status_code == 200:
            print("Authentication successful!")
            return True
        else:
            print("Authentication failed! Please try again.")

def run():
    auth_url = "http://localhost:5000/auth"  # Authentication server URL
    if authenticate_user(auth_url):
        # Create and start Mininet network
        topo = CustomTopo()
        
        # Set the controller IP and port for OpenDaylight
        controller_ip = '10.3.160.106'
        controller_port = 6653
        
        net = Mininet(topo=topo, controller=None, switch=OVSSwitch)
        
        # Add the OpenDaylight controller
        odl_controller = net.addController('c0', controller=RemoteController, ip=controller_ip, port=controller_port)

        try:
            # Start the network
            net.start()
            print(f"Connected to the OpenDaylight controller at {controller_ip}:{controller_port}")
            CLI(net)  # Launch Mininet CLI
        except Exception as e:
            # Handle and display errors related to network start or controller connection
            print(f"An error occurred: {e}")
        finally:
            # Stop the network regardless of success or failure
            net.stop()

if __name__ == '__main__':
    setLogLevel('info')  # Set Mininet log level
    run()
