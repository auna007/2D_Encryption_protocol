from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.topo import Topo
import requests
import os

class CustomTopo(Topo):
    def build(self):
        # Define hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        
        # Define switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        
        # Add links between hosts and switches
        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(h3, s3)
        
        # Optionally, add inter-switch links (depending on the topology you want)
        # self.addLink(s1, s2)
        # self.addLink(s2, s3)

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

def run_tcpdump(net):
    """Run tcpdump on each host and switch interface to capture packets."""
    print("*** Starting packet capture")

    # Create a folder to store tcpdump files
    if not os.path.exists('pcaps'):
        os.makedirs('pcaps')

    # Start tcpdump on each host's interface
    for host in net.hosts:
        host.cmd(f'tcpdump -i {host.defaultIntf()} -w pcaps/{host.name}_traffic.pcap &')
        print(f"Started tcpdump on {host.name}")

    # Start tcpdump on each switch interface
    for switch in net.switches:
        for intf in switch.intfList():
            switch.cmd(f'tcpdump -i {intf} -w pcaps/{switch.name}_{intf}_traffic.pcap &')
            print(f"Started tcpdump on {switch.name} interface {intf}")

    # Optionally, capture traffic between switches and the controller (on localhost)
    # Since it's a remote controller, you might need to capture on the controller side separately.
    # This captures OpenFlow messages between switch and controller, if desired:
    controller_ip = '127.0.0.1'
    net.get('s1').cmd(f'tcpdump -i s1-eth1 host {controller_ip} -w pcaps/s1_controller_traffic.pcap &')
    print(f"Started tcpdump on switch-to-controller communication")

def stop_tcpdump(net):
    """Stop all tcpdump processes."""
    print("*** Stopping packet capture")
    net.hosts[0].cmd('killall tcpdump')

def run():
    auth_url = "http://localhost:5000/auth"  # Authentication server URL
    if authenticate_user(auth_url):
        # Create and start Mininet network
        topo = CustomTopo()
        net = Mininet(topo=topo, controller=RemoteController, switch=OVSSwitch)
        controller_ip = '127.0.0.1'
        controller_port = 6653
        
        # Add the remote controller
        net.addController('c0', ip=controller_ip, port=controller_port)

        try:
            # Start the network
            net.start()
            print(f"Connected to the controller at {controller_ip}:{controller_port}")
            
            # Start capturing packets using tcpdump
            run_tcpdump(net)
            
            # Start Mininet CLI for manual interaction and testing
            CLI(net)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Stop tcpdump and the network after exiting CLI
            stop_tcpdump(net)
            net.stop()

if __name__ == '__main__':
    setLogLevel('info')  # Set Mininet log level
    run()
