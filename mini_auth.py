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
        
        # Define switch
        s1 = self.addSwitch('s1')
        
        # Add links
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)

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
        net = Mininet(topo=topo, controller=RemoteController, switch=OVSSwitch)
        controller_ip = '127.0.0.1'
        controller_port = 6653
        
        # Add the controller
        net.addController('c0', ip=controller_ip, port=controller_port)

        try:
            # Start the network
            net.start()
            print(f"Connected to the controller at {controller_ip}:{controller_port}")
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
