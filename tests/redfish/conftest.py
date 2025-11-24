import pytest
import requests

class RedfishClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.verify = False
        
    def authenticate(self):
        auth_url = f"{self.base_url}/redfish/v1/SessionService/Sessions"
        auth_data = {"UserName": self.username, "Password": self.password}
        
        response = self.session.post(auth_url, json=auth_data)
        
        if response.status_code == 200:
            self.session.headers.update({'X-Auth-Token': response.headers.get('X-Auth-Token')})
            return True
        
        return False

@pytest.fixture(scope="session")
def redfish_client():
    client = RedfishClient("https://localhost:2443", "root", "0penBmc")
    assert client.authenticate()
    return client