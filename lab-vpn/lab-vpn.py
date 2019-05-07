#!/usr/bin/env python

# author: greyshell
# description: use openvpn to access offensive security labs

import base64
import optparse
import subprocess
import time

import pexpect

# setting up emails
emailFrom = 'enter your email address'
emailFromEncodedPass = 'enter base64 encoded password'


class LoginVpn(object):
    def __init__(self):
        self.user = ""
        self.password = ""
        self.command = ""

    def parse_input(self):
        parser = optparse.OptionParser('Usage %prog -p <credential> -c <vpn config> -e <email to send notification>')
        parser.add_option('-p', dest='tgtPass', type='string',
                          help='specify creds.txt, username and password are separated by newline')
        parser.add_option('-c', dest='tgtConfig', type='string', help='specify lab.ovpn')
        parser.add_option('-e', dest='tgtEmailTo', type='string', help='specify email to send the notification')

        (options, args) = parser.parse_args()
        tgtPass = options.tgtPass
        tgtConfig = options.tgtConfig
        tgtEmailTo = options.tgtEmailTo

        if tgtEmailTo is None:
            print
            parser.usage
            exit(0)

        if tgtPass is None:
            print
            parser.usage
            exit(0)

        elif tgtConfig is None:
            print
            parser.usage
            exit(0)

        command = 'openvpn ' + tgtConfig

        j = []
        f = open(tgtPass, 'r')
        for val in f:
            j.append(val)

        self.command = command
        self.user = j[0].strip('\n')
        self.password = j[1].strip('\n')

        return tgtEmailTo

    def coreEngine(self, emailFrom, emailFromPass, emailTo):
        try:
            print
            '[+] connecting to vpn ...'
            # sending email notification, hardcoded the message files
            TST = 'sendEmail -f ' + emailFrom + ' -t ' + emailTo + ' -u \'logged-In\' -o ' \
                                                                   'message-file=\'lab-login-msg.txt\' -s_list ' \
                                                                   'smtp.gmail.com:587 -o tls=yes -xu ' + emailFrom + \
                  " -xp " + emailFromPass
            subprocess.check_output(TST, shell=True)
            print
            "[+] sent email notification .."
            print
            '[+] enjoy the lab, to disconnect press ctrl+c ...'

            i = pexpect.spawn(self.command)
            i.expect_exact('Enter')
            i.sendline(self.user)
            i.expect_exact('Password')
            i.sendline(self.password)

            # delay for 1 day
            time.sleep(3600 * 24)

        except KeyboardInterrupt:
            print
            "[+] received ctrl+c, disconnecting from lab ..."
            TST = "sendEmail -f " + emailFrom + " -t " + emailTo + " -u 'logged-Out' -o " \
                                                                   "message-file='lab-logout-msg.txt' -s_list " \
                                                                   "smtp.gmail.com:587 -o tls=yes -xu " + emailFrom + \
                  " -xp " + emailFromPass
            subprocess.check_output(TST, shell=True)
            print
            "[+] sent email notification .."

        except Exception as e:
            print
            '[x] error occurs while connecting vpn lab !!'
            print
            e

        return


if __name__ == '__main__':
    instance = LoginVpn()
    emailTo = instance.parse_input()
    emailFromPass = base64.b64decode(emailFromEncodedPass)
    instance.coreEngine(emailFrom, emailFromPass, emailTo)
    # end main
