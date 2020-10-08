#!/usr/bin/env python3

'''
Utility script used to test out the Maximum frame size an interface on a VM
can transmit
'''
import argparse
import ipaddress
import logging
import platform
import os


logger = logging.getLogger(__name__)
logger.root.setLevel(logging.INFO)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i',
        '--ip',
        dest='ip',
        default='127.0.0.1',
        help='Specify the target network interface ip address'
    )

    parser.add_argument(
        '-m',
        '--mtu-ceiling',
        dest='mtu_ceiling',
        default='1500',
        help='specify the biggest MTU we want to try out'
    )

    args = parser.parse_args()
    if args.ip and args.mtu_ceiling:
        ip = args.ip
        mtu_ceiling_value = int(args.mtu_ceiling)

    try:
        ipaddress.IPv4Address(ip)
    except ValueError:
        raise Exception("Ip address: {} is invalid".format(ip))

    mtu_tested = []

    # mtu can range between 1200 to anything reasonable
    # maximum packet size we can send is 65507
    # lets compute the mtu over an 8byte interval
    for mtu in range(1200, mtu_ceiling_value, 8):
        command_string = 'ping -M do -s {} {}'.format(mtu, ip)
        current_os = platform.system().lower()

        # we only need to send a single ping request. so based on os-type,
        # let us specify the argument to use
        if current_os == "windows":
            command_string += " -n 1"
        else:
            command_string += " -c 1"

        result = os.system(command_string) # refactor this to use a subprocess
        if result == 0:
            mtu_tested.append(mtu)
        else:
            logger.info("MTU cannot be above this limit {}".format(mtu))
            break

    print("Best computed MTU size is {}".format(mtu_tested[-1]))


if __name__ == '__main__':
    main()