import pytest
import requests
import logging
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from conftest import RedfishClient

logger = logging.getLogger(__name__)

class TestRedfishAuthentication:
    def test_authentication_success(self, redfish_client):
        assert redfish_client.authenticated == True
        assert redfish_client.token is not None
        logger.info("Authentication successful")

    def test_authentication_response_code(self, redfish_client):
        response = redfish_client.session.get(f"{redfish_client.base_url}/redfish/v1/")
        assert response.status_code == 200
        logger.info("Response code 200 for authenticated request")

class TestSystemInfo:
    def test_get_system_info_status_code(self, redfish_client):
        system_info = redfish_client.get("/redfish/v1/Systems/system")
        assert system_info is not None
        logger.info("System info retrieved successfully")
    
    def test_system_info_contains_status_and_powerstate(self, system_info):
        if system_info:
            assert "Status" in system_info
            assert "PowerState" in system_info
            logger.info(f"System status: {system_info.get('Status')}")
            logger.info(f"Power state: {system_info.get('PowerState')}")
        else:
            pytest.skip("System info not available")
    
    def test_system_info_structure(self, system_info):
        if system_info:
            required_fields = ["Id", "Name", "Status", "PowerState"]
            
            for field in required_fields:
                assert field in system_info, f"Missing required field: {field}"
            
            logger.info("All required fields present in response")
        else:
            pytest.skip("System info not available")

class TestPowerManagement:
    def test_power_state_reading(self, redfish_client):
        system_info = redfish_client.get("/redfish/v1/Systems/system")
        if system_info:
            power_state = system_info.get("PowerState")
            valid_states = ["On", "Off", "PoweringOn", "PoweringOff", "Paused", "Reset"]
            assert power_state in valid_states, f"Unknown power state: {power_state}"
            logger.info(f"Current power state: {power_state}")
        else:
            pytest.skip("System info not available")
    
    def test_power_control_endpoint_accessible(self, redfish_client):
        power_control_url = "/redfish/v1/Systems/system/Actions/ComputerSystem.Reset"
        test_data = {"ResetType": "On"}
        
        response = redfish_client.post(power_control_url, test_data)
        
        assert response is not None
        logger.info(f"Power control endpoint accessible, status code: {response.status_code}")
    
    def test_power_command_validation(self, redfish_client):
        power_control_url = "/redfish/v1/Systems/system/Actions/ComputerSystem.Reset"
        
        safe_commands = ["On", "GracefulRestart"]
        
        for command in safe_commands:
            test_data = {"ResetType": command}
            response = redfish_client.post(power_control_url, test_data)
            
            if response is not None:
                assert response.status_code != 400, f"Command {command} is invalid"
                logger.info(f"Command {command} accepted, code: {response.status_code}")

class TestSystemComponents:
    def test_system_processor_info(self, redfish_client):
        system_info = redfish_client.get("/redfish/v1/Systems/system")
        if system_info:
            processor_summary = system_info.get("ProcessorSummary", {})
            count = processor_summary.get("Count", 0)
            logger.info(f"Processor count: {count}")
        
        processors_data = redfish_client.get("/redfish/v1/Systems/system/Processors")
        if processors_data:
            assert "Members" in processors_data
            logger.info("Processors endpoint available")
        else:
            pytest.skip("Processors endpoint not available")
    
    def test_system_memory_info(self, redfish_client):
        system_info = redfish_client.get("/redfish/v1/Systems/system")
        if system_info:
            memory_summary = system_info.get("MemorySummary", {})
            total_memory = memory_summary.get("TotalSystemMemoryGiB", 0)
            logger.info(f"Total system memory: {total_memory} GiB")
        
        memory_data = redfish_client.get("/redfish/v1/Systems/system/Memory")
        if memory_data:
            assert "Members" in memory_data
            logger.info("Memory endpoint available")
        else:
            pytest.skip("Memory endpoint not available")
    
class TestChassisInfo:
    def test_chassis_discovery(self, redfish_client):
        chassis_data = redfish_client.get("/redfish/v1/Chassis")
        if chassis_data and "Members" in chassis_data:
            assert len(chassis_data["Members"]) > 0
            
            first_chassis = chassis_data["Members"][0]
            chassis_detail = redfish_client.get(first_chassis["@odata.id"])
            
            if chassis_detail:
                assert "Name" in chassis_detail
                logger.info(f"Found chassis: {chassis_detail.get('Name')}")
        else:
            pytest.skip("Chassis endpoint not available")
        
    def test_chassis_thermal(self, redfish_client):
        chassis_data = redfish_client.get("/redfish/v1/Chassis")
        if chassis_data and "Members" in chassis_data:
            first_chassis = chassis_data["Members"][0]
            chassis_detail = redfish_client.get(first_chassis["@odata.id"])
            
            if chassis_detail and "Thermal" in chassis_detail:
                thermal_url = chassis_detail["Thermal"]["@odata.id"]
                thermal_data = redfish_client.get(thermal_url)
                
                if thermal_data:
                    logger.info("Thermal information available")
                    
                    if "Temperatures" in thermal_data:
                        logger.info(f"Found {len(thermal_data['Temperatures'])} temperature sensors")

                    if "Fans" in thermal_data:
                        logger.info(f"Found {len(thermal_data['Fans'])} fans")
                else:
                    logger.info("Thermal endpoint not accessible")
            else:
                logger.info("Thermal information not available in chassis")
        else:
            pytest.skip("Chassis endpoint not available")

class TestErrorHandling:
    def test_invalid_authentication(self):
        invalid_client = RedfishClient(
            base_url="https://localhost:2443",
            username="wrong_user", 
            password="wrong_password"
        )
        
        result = invalid_client.authenticate()

        assert result == False, "Authentication with wrong credentials should return False"
        assert invalid_client.authenticated == False, "Authenticated flag should be False"
        
        logger.info("Invalid authentication handling works correctly")
    
    def test_invalid_endpoint(self, redfish_client):
        response = redfish_client.session.get(
            f"{redfish_client.base_url}/redfish/v1/InvalidEndpoint"
        )
        
        assert response.status_code == 404
        logger.info("Invalid endpoint handling works correctly")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])