from locust import HttpUser, task, between
import base64

class OpenBMCTestUser(HttpUser):
    wait_time = between(1, 3)
    host = "https://localhost:2443"
    
    def on_start(self):
        credentials = "root:0penBmc"
        self.auth_header = {
            "Authorization": f"Basic {base64.b64encode(credentials.encode()).decode()}"
        }
    
    @task(3)
    def get_system_info(self):
        with self.client.get("/redfish/v1/Systems/system", 
                             headers=self.auth_header,
                             verify=False,
                             name="[BMC] System",
                             catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status code: {response.status_code}")
    
    @task(2)
    def get_power_state(self):
        with self.client.get("/redfish/v1/Systems/system",
                             headers=self.auth_header,
                             verify=False,
                             name="[BMC] Power State",
                             catch_response=True) as response:
            if response.status_code == 200:
                try:
                    json_response = response.json()
                    power_state = json_response.get("PowerState")
                    if power_state:
                        response.success()
                    else:
                        response.failure("PowerState not found in response")
                except ValueError:
                    response.failure("Invalid JSON response")
            else:
                response.failure(f"Status code: {response.status_code}")