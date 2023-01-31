#!/usr/bin/python3

from settings import *
if 'ssh_targets' in globals():
    if ssh_targets != []:
        from netmiko import ConnectHandler
else:
    ssh_targets = []
import requests
from time import sleep
from datetime import datetime


def run_ios_command(device_type, host, username, password, command):

    # Log into a device and execute a command
    # device_type 'cisco_ios' works with Cisco CLI

    try:
        net_connect = ConnectHandler(device_type=device_type, host=host, username=username, password=password)
        net_output = net_connect.send_command(command)
        net_connect.disconnect()
        net_output = f'{host}:{command}:\n' + net_output
        net_output = net_output.splitlines()
        net_output = '\n'.join(str(elem) for elem in net_output[0:min(4, len(net_output))]) + '\n'
    except Exception as e:
        net_output = e.args[0]

    return net_output


if __name__ == '__main__':

    t = datetime.now()
    filename = f'{t.month:02}-{t.day:02}.{t.hour:02}:{t.minute:02}.chatbot.log'
    print(f'HTTP Test Targets\n{urls}')
    print(f'SSH Test Targets\n{ssh_targets}')
    print(f'Test results are being logged to {filename}.  Only failed attempts will be printed to the screen.')

    if 'urls' not in globals():
        urls = []

    duration = int(input(f'How many minutes do you want the test to run? [{duration}]:') or duration)
    wait_time = int(input(f'How many seconds do you want to wait between iterations? [{wait_time}]:') or wait_time)
    iterations = int(duration * 60 / wait_time)

    while iterations > -1:

        t = datetime.now()
        outfile = open(filename, 'a')
        outfile.write(f'{t.month:02}/{t.day:02} {t.hour:02}:{t.minute:02}\n')

        # Get all websites and print status codes

        for url in urls:
            try:
                junk = requests.get(url, timeout=20)
                outfile.write(f'{url}: {junk.status_code} - {junk.reason}\n')
                if junk.status_code != 200:
                    print(f'{url} get error: {junk.reason}')
            except Exception as e:
                error_out = f'{url}: Python Exception Error [{e}]\n'
                outfile.write(error_out)
                print(error_out)

        # Get SSH data

        for ssh_target in ssh_targets:
            output = run_ios_command('cisco_ios', ssh_target, ssh_user, ssh_password, command)
            outfile.write(output)

        outfile.close()

        print()
        if iterations > 0:
            print(f'This test will run {iterations} more time(s).')
            print(f'This test will re-run in {wait_time} seconds.  Break to exit.')
            sleep(wait_time)

        iterations -= 1

    print('Test complete.')
