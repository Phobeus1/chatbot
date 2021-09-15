#!python3

from includes import ssh_user, ssh_password, ssh_target, urls, waittime
from netmiko import ConnectHandler
import requests
from time import sleep
from datetime import datetime

def run_ios_command(device_type, host, username, password, command):

    # Log into a device and execute a command
    # device_type 'cisco_ios' works with Cisco CLI

    try:
        net_connect = ConnectHandler(device_type=device_type, host=host, username=username, password=password)
        output = net_connect.send_command(command).split('\n',2)[1]+'\n'
        net_connect.disconnect()
    except Exception as e:
        output = e.args[0]

    return output

if __name__ == '__main__':

    t = datetime.now()

    filename = f'{t.month}-{t.day}.{t.hour}:{t.minute}.chatbot.log'

    while True:

        t = datetime.now()

        outfile = open(filename, 'a')

        outfile.write(f'{t.month}/{t.day} {t.hour}:{t.minute}\n')

        # Get all websites and print status codes

        for x in urls:
            try:
                junk = requests.get(x, timeout=20)
                outfile.write(f'{x}: {junk.status_code} - {junk.reason}\n')
            except Exception as e:
                outfile.write(f'{x}: Python Exception Error [{e}]\n')

        # Get SSH data

        output = run_ios_command('cisco_ios', ssh_target, ssh_user, ssh_password, 'show running')
        outfile.write(output)
        outfile.close()

        print(f'\nThis test will re-run in {waittime} seconds.  Break to exit.')
        sleep(waittime)

