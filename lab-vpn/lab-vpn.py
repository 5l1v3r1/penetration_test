#!/usr/bin/env python3

# author: greyshell
# description: use openvpn to access offensive security labs


import argparse
import base64
import json
import subprocess
import sys
import time

import pexpect
from colorama import Fore

# global constant variable
PROGRAM_LOGO = """
 _      ____  _____    __  _______  __  _ 
| |__  / () \ | () )   \ \/ /| ()_)|  \| |
|____|/__/\__\|_()_)    \__/ |_|   |_|\__|
"""


class UserInput:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
                description="automate the openvpn lab connection")
        self.parser.add_argument("-p", "--vpn_credential", metavar="", help="provide vpn credential in a json file ",
                                 required=True)
        self.parser.add_argument("-c", "--config", metavar="", help="provide a ovpn file for the lab", required=True)
        self.parser.add_argument("-e", "--email_credential", metavar="", help="provide email credential in a json file",
                                 required=True)
        self.parser.add_argument("-t", "--email_to", metavar="", help="provide a email to send the notification",
                                 required=True)
        self.parser.add_argument("-d", "--set_dns", metavar="", help="set the dns to resolv.conf ", required=False)


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
        self.dns = ""

    def get_parameters(self, vpn, config_file, email, email_to, dns):
        """
        retrieve the value from the input
        :param vpn: dict
        :param config_file: string
        :param email: dict
        :param email_to: string
        :param dns: string
        :return: None
        """
        self.email_to = email_to
        self.email_from = email["email_from"]

        self.email_password = base64.b64decode(email["email_password"].encode()).decode()  # convert bytes to string
        self.login_message = email["login_message"]
        self.logout_message = email["logout_message"]

        self.vpn_user = vpn["vpn_user"]
        self.vpn_password = vpn["vpn_password"]

        self.vpn_config = config_file

        self.vpn_command = "openvpn" + " " + self.vpn_config
        self.dns = dns

    def lab_connection(self):
        """
        connect to the vpn
        :return: None
        """
        try:
            if self.dns:
                print(Fore.GREEN, f"[+] set the dns entry {self.dns} into /etc/resolve.conf")
                set_dns_command = "sed -i \'1s/^/nameserver " + self.dns + "\\n/\' /etc/resolv.conf"
                subprocess.check_output(set_dns_command, shell=True)

            print(Fore.GREEN, f"[+] sending email notification ...")
            send_email_command = "sendEmail -f " + self.email_from + " -t " + self.email_to + \
                                 " -u \'logged-In\' -o message-file=" + self.login_message + \
                                 " -s smtp.gmail.com:587 -o tls=yes -xu " + self.email_from + \
                                 " -xp " + self.email_password

            subprocess.check_output(send_email_command, shell=True)

            print(Fore.LIGHTBLUE_EX, f"[*] connected to the lab, press ctrl+c to disconnect from the lab")

            # connect to the lab
            i = pexpect.spawn(self.vpn_command)
            i.expect_exact("Enter")
            i.sendline(self.vpn_user)
            i.expect_exact("Password")
            i.sendline(self.vpn_password)

            # delay for 1 day
            time.sleep(3600 * 24)

        except KeyboardInterrupt:
            print(Fore.RED, f"[*] received ctrl+c, disconnecting from lab ")
            send_email_command = "sendEmail -f " + self.email_from + " -t " + self.email_to + \
                                 " -u \'logged-Out\' -o message-file=" + self.logout_message + \
                                 " -s smtp.gmail.com:587 -o tls=yes -xu " + self.email_from + \
                                 " -xp " + self.email_password
            subprocess.check_output(send_email_command, shell=True)
            print(Fore.GREEN, f"[*] sent email notification to {self.email_to} ")

            if self.dns:
                print(Fore.GREEN, f"[+] unset the dns entry {self.dns} from resolve.conf ")
                unset_dns_command = "sed -i '1d' /etc/resolv.conf"
                subprocess.check_output(unset_dns_command, shell=True)

        except Exception as e:
            print(Fore.MAGENTA, f"[x] error occurs while connecting vpn !")
            print(e)


if __name__ == "__main__":
    my_input = UserInput()
    args = my_input.parser.parse_args()

    if len(sys.argv) == 1:
        my_input.parser.print_help(sys.stderr)
        sys.exit(1)

    if not args.set_dns:
        lab_dns = None
    else:
        lab_dns = args.set_dns

    if args.vpn_credential and args.config and args.email_credential and args.email_to:
        with open(args.vpn_credential) as f:
            vpn_credential = json.load(f)
        with open(args.email_credential) as f:
            email_credential = json.load(f)

        # display program logo
        print(Fore.GREEN, f"{PROGRAM_LOGO}")

        conn = LoginVpn()
        conn.get_parameters(vpn_credential, args.config, email_credential, args.email_to, lab_dns)
        conn.lab_connection()

    else:
        my_input.parser.print_help(sys.stderr)
