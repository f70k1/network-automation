import time
from netmiko import ConnectHandler
from getpass import getpass

from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException

print ("Monitor Capture \n This tool sniffs traffic on an Interface")

IP_ADDRESS_OF_DEVICE = input("IP-Address of Device: ")
USERNAME = input("Enter your SSH-Username: ")
PASSWORD = getpass("Enter your SSH-Password: ")
TIMEOUT = int(input("How long shoud the Capture run [sec]: "))

SCP_IP = input("IP-SCP-Server: " )
SCP_USERNAME = input("Enter your SCP-Username: ")
SCP_PASSWORD = getpass("Enter your SCP-Password: ")

IOS = {
    "device_type": "cisco_ios",
    "ip": IP_ADDRESS_OF_DEVICE,
    "username": USERNAME,
    "password": PASSWORD,
}

for i in range (1,2):
    try:
        net_connect = ConnectHandler(**IOS)
    except (AuthenticationException):
        print ("Authentication failure: " + IP_ADDRESS_OF_DEVICE)
        continue
    except (NetMikoTimeoutException):
        print ("Timeout to device: " + IP_ADDRESS_OF_DEVICE)
        continue
    except (EOFError):
        print ("End of file while attempting device: " + IP_ADDRESS_OF_DEVICE)
        continue
    except (SSHException):
        print ("SSH Issue. Are you sure SSH is enabled?:  " + IP_ADDRESS_OF_DEVICE)
        continue
    except Exception as unknown_error:
        print ("Some other error " + IP_ADDRESS_OF_DEVICE)
        continue

    output = net_connect.send_command("show ip int brief")
    print (output)
    output = net_connect.send_command("show int des")
    print (output)

    INTERFACE = input("Which Interface: ")

    net_connect.send_command("monitor capture CAP interface " + INTERFACE + " both")
    net_connect.send_command("monitor capture CAP match any")
    print ("Monitor IP: " + IP_ADDRESS_OF_DEVICE + " Interface: " + INTERFACE + " start")
    net_connect.send_command("monitor capture CAP start")

    for t in range (1, TIMEOUT+1):
        print ("*" * t)
        time.sleep(1)

    net_connect.send_command("monitor capture CAP stop")
    print ("Monitor IP: " + IP_ADDRESS_OF_DEVICE + " Interface: " + INTERFACE + " stop")
    output = net_connect.send_command("show monitor capture CAP buffer")
    print (output)
    #net_connect.send_command("monitor capture CAP export ftp://"+ FTP_IP +"/CAP.pcap")
    output = (net_connect.send_command("monitor capture CAP export scp://" + SCP_USERNAME + ":" + SCP_PASSWORD + "@" + SCP_IP +"/CAP.pcap"))
    #output = (net_connect.send_command("monitor capture CAP export scp://" + SCP_USERNAME + ":" + SCP_PASSWORD + "@" + SCP_IP +"/CAP.pcap", delay_factor=100))
    print (output)
    net_connect.send_command("no monitor capture CAP")
    net_connect.disconnect()
