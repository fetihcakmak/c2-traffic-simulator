#!/usr/bin/env python3
import argparse
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from simulator.http_beacon import HttpBeacon, COBALT_STRIKE_PROFILE
from simulator.dns_beacon import DnsBeacon

RED    = "\033[91m"
GREEN  = "\033[92m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

BANNER = f"""{BOLD}{RED}
   ___ ___     ___ _                 _      _           
  / __|_  )   / __(_)_ __ _  _ _ __ | |__ _| |_ ___ _ _ 
 | (__ / /   \__ \ | '  \ || | '  \| / _` |  _/ _ \ '_|
  \___/___|  |___/_|_|_|_\_,_|_|_|_|_\__,_|\__\___/_|  
       C2 TRAFFIC SIMULATOR v1.0 [BLUE TEAM TESTER]{RESET}
"""

def main():
    parser = argparse.ArgumentParser(description='C2 Traffic Simulator')
    parser.add_argument('--mode', choices=['http', 'dns'], required=True, help='Beacon mode')
    parser.add_argument('--target', required=True, help='Target URL or Domain')
    parser.add_argument('--count', type=int, default=5, help='Number of beacons to send')
    
    args = parser.parse_args()
    print(BANNER)
    
    if args.mode == 'http':
        beacon = HttpBeacon(target_url=args.target)
        for i in range(args.count):
            res = beacon.send_beacon()
            print(f"{CYAN}[HTTP]{RESET} {res['method']} {res['url']} -> {res['status']} (Sleep: {res['sleep_time']:.1f}s)")
            time.sleep(res['sleep_time'] if i < args.count - 1 else 0)
            
    elif args.mode == 'dns':
        beacon = DnsBeacon(domain=args.target)
        for i in range(args.count):
            res = beacon.send_beacon()
            print(f"{CYAN}[DNS]{RESET} Query: {res['query'][:50]}... -> {res['status']}")
            time.sleep(res['sleep_time'] if i < args.count - 1 else 0)

if __name__ == '__main__':
    main()
