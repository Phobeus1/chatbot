#!python3

from includes import ssh_user, ssh_password, ssh_target, urls, waittime
from netmiko import ConnectHandler
import requests
from time import sleep

def run_ios_command(device_type, host, username, password, command):

    # Log into a device and execute a command
    # device_type 'cisco_ios' works with Cisco CLI

    net_connect = ConnectHandler(device_type=device_type, host=host, username=username, password=password)
    output = net_connect.send_command(command)
    net_connect.disconnect()
    return output

if __name__ == '__main__':

    while True:

        # Get all websites and print status codes

        for x in urls:
            try:
                junk = requests.get(x, timeout=20)
                print(f'{x}: {junk.status_code} - {junk.reason}')
            except Exception as e:
                print(f'\n{x}: Python Exception Error [{e}]\n')

        # Get SSH data

        output = run_ios_command('cisco_ios', ssh_target, ssh_user, ssh_password, 'show int | t')
        print(output)

        print(f'\nThis test will re-run in {waittime} seconds.  Break to exit.')
        sleep(waittime)

