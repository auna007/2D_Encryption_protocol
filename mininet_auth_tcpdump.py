from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.topo import Topo
import requests
import os

# Simulate DNA encryption and decryption
def dna_encrypt(data):
    """Dummy DNA encryption function (replace with actual DNA encryption implementation)."""
    return ''.join(reversed(data))  # Simple reverse for demonstration

def dna_decrypt(data):
    """Dummy DNA decryption function (replace with actual DNA decryption implementation)."""
    return ''.join(reversed(data))  # Reverse back for decryption

# Custom topology with three switches and three hosts
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
        username = input("Enter username: ")
        password = input("Enter password: ")
        totp_code = input("Enter TOTP code: ")

        data = {
            "username": username,
            "password": password,
            "totp_code": totp_code
        }

        response = requests.post(auth_url, json=data)
        print(response.content.decode())

        if response.status_code == 200:
            print("Authentication successful!")
            return True
        else:
            print("Authentication failed! Please try again.")

def run_tcpdump_and_dna_encryption(net):
    """Run tcpdump on each host and simulate DNA encryption and decryption."""
    print("*** Starting tcpdump and DNA encryption")

    # Create a folder to store tcpdump files if it doesn't exist
    if not os.path.exists('pcaps'):
        os.makedirs('pcaps')

    # Start tcpdump on each host's interface and simulate encryption
    for host in net.hosts:
        interface = host.defaultIntf()
        tcpdump_cmd = f'tcpdump -i {interface} -w pcaps/{host.name}_traffic.pcap &'
        host.cmd(tcpdump_cmd)
        print(f"Started tcpdump on {host.name} interface {interface}")

        # Simulate DNA encryption on outgoing traffic
        traffic = f"Simulated traffic from {host.name}"
        encrypted_traffic = dna_encrypt(traffic)
        print(f"Encrypting data from {host.name}: {encrypted_traffic}")

    # Start tcpdump on each switch interface
    for switch in net.switches:
        for intf in switch.intfList():
            tcpdump_cmd = f'tcpdump -i {intf} -w pcaps/{switch.name}_{intf}_traffic.pcap &'
            switch.cmd(tcpdump_cmd)
            print(f"Started tcpdump on {switch.name} interface {intf}")

def stop_tcpdump(net):
    """Stop all tcpdump processes."""
    print("*** Stopping tcpdump")
    net.hosts[0].cmd('killall tcpdump')

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
        odl_controller = net.addController('c0', controller=RemoteController, 
                                           ip=controller_ip, port=controller_port)

        try:
            # Start the network
            net.start()
            print(f"Connected to the OpenDaylight controller at {controller_ip}:{controller_port}")
            
            # Start capturing packets using tcpdump and simulating DNA encryption
            run_tcpdump_and_dna_encryption(net)
            
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
