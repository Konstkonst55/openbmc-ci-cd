import pytest
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RedfishClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.verify = False
        self.token = None
        self.authenticated = False
        
    def authenticate(self):
        try:
            auth_url = f"{self.base_url}/redfish/v1/SessionService/Sessions"
            auth_data = {"UserName": self.username, "Password": self.password}
            
            response = self.session.post(auth_url, json=auth_data)
            
            if response.status_code in [200, 201]:
                self.token = response.headers.get('X-Auth-Token')
                if self.token:
                    self.session.headers.update({'X-Auth-Token': self.token})
                self.authenticated = True
                return True
            
            logger.warning(f"Authentication failed with status code: {response.status_code}")
            return False
            
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return False
    
    def get(self, endpoint):
        try:
            url = f"{self.base_url}{endpoint}"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"GET request failed: {e}")
            return None
    
    def post(self, endpoint, data):
        try:
            url = f"{self.base_url}{endpoint}"
            response = self.session.post(url, json=data)
            return response
        except Exception as e:
            logger.error(f"POST request failed: {e}")
            return None

@pytest.fixture(scope="session")
def redfish_client():
    client = RedfishClient("https://localhost:2443", "root", "0penBmc")
    if not client.authenticate():
        pytest.skip("Redfish authentication failed - skipping Redfish tests")
    return client

@pytest.fixture(scope="function")
def system_info(redfish_client):
    return redfish_client.get("/redfish/v1/Systems/system")