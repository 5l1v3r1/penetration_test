#!/usr/bin/env python3

# author: greyshell
# description: use openvpn to access offensive security labs


import sys
import base64
import argparse
import subprocess
import time
import pexpect
import json
from colorama import Fore


class UserInput:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="automate the openvpn lab connection")
        self.parser.add_argument("-p", "--vpn_credential", metavar="", help="provide vpn credential in a json file ")
        self.parser.add_argument("-c", "--config", metavar="", help="provide a ovpn file for the lab")
        self.parser.add_argument("-e", "--email_credential", metavar="", help="provide email credential in a json file")
        self.parser.add_argument("-t", "--email_to", metavar="", help="provide a email to send the notification")


class LoginVpn:
    def __init__(self):
        self.email_to = ""

        self.email_from = ""
        self.email_password = ""
        self.login_message = ""
        self.logout_message = ""

        self.vpn_user = ""
        self.vpn_password = ""
        self.vpn_config = ""

        self.vpn_command = ""

    def get_parameters(self, vpn, config_file, email, email_to):
        self.email_to = email_to
        self.email_from = email['email_from']

        self.email_password = base64.b64decode(email['email_password'].encode()).decode()  # convert bytes to string
        self.login_message = email['login_message']
        self.logout_message = email['logout_message']

        self.vpn_user = vpn['vpn_user']
        self.vpn_password = vpn['vpn_password']

        self.vpn_config = config_file

        self.vpn_command = "openvpn" + " " + self.vpn_config

    def lab_connection(self):
        try:
            print(Fore.GREEN, f'[+] connecting to vpn ...')

            print(Fore.GREEN, f'[+] sending email notification ...')
            send_email_command = "sendEmail -f " + self.email_from + " -t " + self.email_to + \
                                 " -u \'logged-In\' -o message-file=" + self.login_message + \
                                 " -s smtp.gmail.com:587 -o tls=yes -xu " + self.email_from + \
                                 " -xp " + self.email_password

            subprocess.check_output(send_email_command, shell=True)

            print(Fore.RED, f'[*] press ctrl+c to disconnect from the lab')

            # connect to the lab
            i = pexpect.spawn(self.vpn_command)
            i.expect_exact('Enter')
            i.sendline(self.vpn_user)
            i.expect_exact('Password')
            i.sendline(self.vpn_password)

            # delay for 1 day
            time.sleep(3600 * 24)

        except KeyboardInterrupt:
            print(Fore.RED, f'[*] received ctrl+c, disconnecting from lab ...')
            send_email_command = "sendEmail -f " + self.email_from + " -t " + self.email_to + \
                                 " -u \'logged-Out\' -o message-file=" + self.logout_message + \
                                 " -s smtp.gmail.com:587 -o tls=yes -xu " + self.email_from + \
                                 " -xp " + self.email_password
            subprocess.check_output(send_email_command, shell=True)
            print(Fore.GREEN, f'[*] sent email notification to {self.email_to} ...')

        except Exception as e:
            print(Fore.MAGENTA, f'[x] error occurs while connecting vpn !')
            print(e)

        return


if __name__ == '__main__':
    my_input = UserInput()
    args = my_input.parser.parse_args()

    if len(sys.argv) == 1:
        my_input.parser.print_help(sys.stderr)
        sys.exit(1)

    if args.vpn_credential and args.config and args.email_credential and args.email_to:
        with open(args.vpn_credential) as f:
            vpn_credential = json.load(f)
        with open(args.email_credential) as f:
            email_credential = json.load(f)

        conn = LoginVpn()
        conn.get_parameters(vpn_credential, args.config, email_credential, args.email_to)
        conn.lab_connection()

    else:
        my_input.parser.print_help(sys.stderr)


