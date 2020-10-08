### MTU Checker

This repo contains a simple python script used to check the maximum size of a
Frame a given network interface can support.

With this information, we can easily set the MTU for an interface as we see it
necessary.

To run this script, simply

python3 mtu_checker.py --ip 127.0.0.1 -m 1500

    `--ip` is the local ip of the interface you wish to check.
    `-m` is the specific mtu size you want to test