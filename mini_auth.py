from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.topo import Topo
import requests

class CustomTopo(Topo):
    def build(self):
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        s1 = self.addSwitch('s1')
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)

def authenticate_user():
    auth_url = "http://localhost:5000/auth"  # Assuming the auth server is on the same machine
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
        print(response.content)
        if response.status_code == 200:
            print("Authentication successful!")
            return True
        else:
            print("Authentication failed! Please try again.")

def run():
    if authenticate_user():
        topo = CustomTopo()
        net = Mininet(topo=topo, controller=RemoteController, switch=OVSSwitch)
        net.addController('c0', ip='127.0.0.1', port=6653)  # Adjust IP if the controller is remote

        net.start()
        CLI(net)
        net.stop()
    else:
        print("Exiting due to failed authentication.")

if __name__ == '__main__':
    setLogLevel('info')
    run()
