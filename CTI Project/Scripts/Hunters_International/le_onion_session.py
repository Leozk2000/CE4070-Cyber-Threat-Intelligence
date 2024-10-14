
import requests


class LeOnionSession:
    """
    Oh wow there's a description here! How cool is that?!
    """

    def __init__(self, port_number: int = 9150):
        self.session = None
        self.create_session(port_number)
        self.check_tor_connection()

    def create_session(self, port_number):
        self.session = requests.Session()
        self.session.proxies = {
            'http': f'socks5h://localhost:{port_number}',
            'https': f'socks5h://localhost:{port_number}'
        }

    def check_tor_connection(self):
        try:
            # Send a request to an IP-checking service
            response = self.session.get('http://httpbin.org/ip')
            response.raise_for_status()
            ip_info = response.json()
            print(
                f"Wonderful :) You're connected to TOR. Your IP is: {ip_info['origin']}")
        except requests.RequestException as e:
            print(f"Oh noes! Failed to connect to TOR: {e}")

    def get(self, url, verify=True):
        try:
            response = self.session.get(url, verify=verify)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            return f"Oh noes! Failed to connect to {url}: {e}"


if __name__ == '__main__':
    tor_session = LeOnionSession()
    response = tor_session.get('http://httpbin.org/ip', verify=False)
    print(response.json())
