#!/usr/local/bin/python3
import cmd
import socket
import time
import logging

import paramiko


def ssh_check():
    print(User, Password)
    with open('switch.txt', 'r') as file:
        IPs = file.readlines()
    for IP in IPs:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(IP.strip(), username=User, password=Password)
        except paramiko.SSHException as e:
            print("{} Password is invalid:{}".format(IP.strip(), e))
            IPs.remove(IP)
        except paramiko.AuthenticationException:
            print("{} Authentication failed for some reason".format(IP.strip()))
            IPs.remove(IP)
        except socket.error as e:
            print("{} Socket connection failed: {}".format(IP.strip(), e))
            IPs.remove(IP)
    return IPs


class command(cmd.Cmd):
    prompt = 'ssh >'

    def do_run(self, command):
        hosts = ssh_check()
        for host in hosts:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host.strip(), username=User, password=Password)
            logging.basicConfig(filename="sample.log", level=logging.DEBUG)
            channel_conn = ssh.invoke_shell()
            output = channel_conn.recv(1024)
            channel_conn.send(command + '\n')
            while not channel_conn.recv_ready():
                time.sleep(3)
            output = channel_conn.recv(1024)
            print('{} {}'.format(host, output.decode()))
            ssh.close()

    def do_bye(self, arg):
        return True

if __name__ == "__main__":

    User = input('Enter your username:')
    Password = input('Enter your password:')
    command().cmdloop()
