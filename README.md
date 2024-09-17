# 2D_Encryption_protocol Read Me File
DNA-Based Diffie-Hellman Encryption Protocol is a proposed encryption technique for securing data during communication in Software Defined Networking Environment.

# Mininet Authentication Project

This project sets up a Mininet network topology with user authentication using username and password before allowing network operations. The project uses the OpenDaylight (ODL) controller.

## Prerequisites

- Python 3.x
- Mininet
- OpenDaylight Controller (ODL)
- Flask
- Sqlite3

## Setup

### 1. Install Mininet

Follow the instructions on the [Mininet website](http://mininet.org/download/) to install Mininet.

### 2. Install OpenDaylight

Download and install OpenDaylight (version: carbon-0.6.4) from the [OpenDaylight website](https://nexus.opendaylight.org/content/repositories/public/org/opendaylight/integration/distribution-karaf/0.6.4-Carbon/distribution-karaf-0.6.4-Carbon.tar.gz).

Extract the downloaded file and navigate to the directory:

```bash
tar -zxvf distribution-karaf-0.6.4-Carbon.tar.gz
cd distribution-karaf-0.6.4-Carbon
```
Install the OpenDayLight:
```bash
./bin/karaf
```

Install the required features in the Karaf console:
```bash
feature:install odl-openflowplugin-all odl-restconf
```
# feature:install odl-restconf odl-openflowplugin-all

# feature:install odl-restconf odl-mdsal-apidocs - used 

If you encountered Java Issue, Follow the below steps to install the right version for the ODL
```bash
sudo apt install openjdk-8-jdk
```

Find and select the path to Java 8:
```bash
sudo update-alternatives --config java
```

Set the JAVA_HOME variable by adding the following lines to your .bashrc (at home) or .bash_profile file:
```bash
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
```

Apply the changes:
```bash
source ~/.bashrc
```

### 3. Install Python Packages
Create a virtual environment (optional but recommended):

```bash
python3 -m venv mininet_env
source mininet_env/bin/activate
```

Install Flask, Requests, Mininet, Qrcode and Pyotp:
```bash
pip install flask requests mininet qrcode pyotp
```

### 4. Seed Users
Run the below command on terminal
```bash
python3 create_db.py
```
The above command will create 3 users in database and print each user along with his secret key on the terminal. each user will have the following:
username, password and secret_key (secret_key will be used for totp).

### 5. Setup Google Authenticator
Run the below command on terminal to get Qrcode image that will be used in Google Authenticator
```bash
python3 generate_qrcode.py
```
You will be prompted to input email (any email can be used, even invalid), secret_key (copy one of the secret keys of the seeded users). The script will create a qrcode and save it in qrcode_image folder as image. The image file will be named using email provided.
You can now go ahead and scan the image in Google Authenticator app.

## Running the Project
### 1. Start the Authentication Server
Open a terminal and run:

```bash
python3 auth_server.py
```
The server will start and listen on http://0.0.0.0:5000.

### 2. Run the Mininet Script
Open another terminal and run:

```bash
python3 mini_auth.py OR use sudo
```
You will be prompted for a username, password and totp. The script will authenticate the user before setting up the Mininet topology.
