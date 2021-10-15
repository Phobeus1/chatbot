#!/usr/bin/python3

from settings import *
from netmiko import ConnectHandler
import requests
from time import sleep
from datetime import datetime

def run_ios_command(device_type, host, username, password, command):

    # Log into a device and execute a command
    # device_type 'cisco_ios' works with Cisco CLI

    try:
        net_connect = ConnectHandler(device_type=device_type, host=host, username=username, password=password)
        output = net_connect.send_command(command)
        net_connect.disconnect()
        output = f'{host}:{command}:\n' + output
        output = output.splitlines()
        output = '\n'.join(str(elem) for elem in output[0:min(4, len(output))]) + '\n'
    except Exception as e:
        output = e.args[0]

    return output

if __name__ == '__main__':

    t = datetime.now()
    filename = f'{t.month:02}-{t.day:02}.{t.hour:02}:{t.minute:02}.chatbot.log'
    if 'duration' in globals():
        iterations = int(duration*60/waittime)
    else:
        iterations = -1
    if 'urls' not in globals():
        urls =[]
    if 'ssh_targets' not in globals():
        ssh_targets = []

    while iterations != 0:

        iterations -= 1
        t = datetime.now()
        outfile = open(filename, 'a')
        outfile.write(f'{t.month:02}/{t.day:02} {t.hour:02}:{t.minute:02}\n')

        # Get all websites and print status codes

        for url in urls:
            try:
                junk = requests.get(url, timeout=20)
                outfile.write(f'{url}: {junk.status_code} - {junk.reason}\n')
            except Exception as e:
                outfile.write(f'{url}: Python Exception Error [{e}]\n')

        # Get SSH data

        for ssh_target in ssh_targets:
            output = run_ios_command('cisco_ios', ssh_target, ssh_user, ssh_password, command)
            outfile.write(output)

        outfile.close()

        print()
        if iterations > 0:
            print(f'This test will run {iterations} more time(s).')
        if iterations != 0:
            print(f'This test will re-run in {waittime} seconds.  Break to exit.')
            sleep(waittime)

    print('Test complete.')