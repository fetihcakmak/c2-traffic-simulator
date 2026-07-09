"""
HTTP Beacon Simulator - Generates synthetic HTTP C2 traffic
"""
import urllib.request
import urllib.parse
import time
import random
import json
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class HttpProfile:
    user_agent: str
    uris: list
    headers: Dict[str, str]

COBALT_STRIKE_PROFILE = HttpProfile(
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    uris=["/api/v1/update", "/jquery-3.3.1.min.js", "/submit.php"],
    headers={"Accept": "*/*", "Connection": "Keep-Alive"}
)

class HttpBeacon:
    def __init__(self, target_url: str, interval: int = 10, jitter: int = 20, profile: HttpProfile = COBALT_STRIKE_PROFILE):
        self.target_url = target_url.rstrip('/')
        self.interval = interval
        self.jitter = jitter
        self.profile = profile
        self.client_id = f"{random.randint(1000, 9999)}"
        
    def _calculate_sleep(self) -> float:
        jitter_percent = self.jitter / 100.0
        jitter_val = self.interval * jitter_percent
        return self.interval + random.uniform(-jitter_val, jitter_val)
        
    def _generate_payload(self) -> bytes:
        data = {
            "id": self.client_id,
            "status": "alive",
            "uptime": random.randint(100, 10000)
        }
        return json.dumps(data).encode('utf-8')

    def send_beacon(self) -> dict:
        """Simulates a single beacon request (doesn't actually require the server to be malicious)"""
        uri = random.choice(self.profile.uris)
        full_url = f"{self.target_url}{uri}?id={self.client_id}"
        
        req = urllib.request.Request(full_url, data=self._generate_payload(), headers=self.profile.headers, method='POST')
        req.add_header('User-Agent', self.profile.user_agent)
        
        start_time = time.time()
        try:
            # We use a short timeout. Even if it fails (ConnectionRefused), we log the attempt for simulation.
            with urllib.request.urlopen(req, timeout=3) as response:
                status = response.status
        except urllib.error.URLError as e:
            status = getattr(e, 'code', 'Connection Failed')
            
        return {
            "url": full_url,
            "method": "POST",
            "status": status,
            "sleep_time": self._calculate_sleep(),
            "bytes_sent": len(self._generate_payload())
        }
