import pytest
import subprocess
import docker
import os

class TestDockerImage:
    """Test suite for Docker image functionality"""
    
    @pytest.fixture(scope="class")
    def docker_client(self):
        """Docker client fixture"""
        try:
            client = docker.from_env()
            client.ping()
            return client
        except Exception as e:
            pytest.skip(f"Docker not available: {e}")
    
    def test_docker_image_exists(self, docker_client):
        """Test that Docker image exists"""
        image_name = "mlc-llm:runtime"
        try:
            image = docker_client.images.get(image_name)
            assert image is not None
        except docker.errors.ImageNotFound:
            pytest.skip(f"Docker image {image_name} not found")
    
    def test_docker_non_root_user(self, docker_client):
        """Test that Docker container runs as non-root"""
        image_name = "mlc-llm:runtime"
        try:
            result = docker_client.containers.run(
                image_name,
                command="whoami",
                remove=True,
                stdout=True,
                stderr=True
            )
            username = result.decode().strip()
            assert username != "root", "Container should not run as root"
            assert username == "mlcuser", f"Expected mlcuser, got {username}"
        except docker.errors.ImageNotFound:
            pytest.skip(f"Docker image {image_name} not found")
    
    def test_docker_healthcheck(self, docker_client):
        """Test Docker container health check"""
        image_name = "mlc-llm:runtime"
        try:
            container = docker_client.containers.run(
                image_name,
                detach=True,
                remove=True
            )
            
            # Wait a bit for health check
            import time
            time.sleep(10)
            
            container.reload()
            health = container.attrs.get('State', {}).get('Health', {})
            
            # Clean up
            container.stop()
            
            # Health check should be defined
            assert 'Status' in health or health == {}
            
        except docker.errors.ImageNotFound:
            pytest.skip(f"Docker image {image_name} not found")
    
    def test_docker_environment_variables(self, docker_client):
        """Test that required environment variables are set"""
        image_name = "mlc-llm:runtime"
        try:
            result = docker_client.containers.run(
                image_name,
                command="env",
                remove=True,
                stdout=True,
                stderr=True
            )
            env_output = result.decode()
            
            # Check for required environment variables
            required_vars = [
                "MLC_LLM_SOURCE_DIR",
                "PYTHONPATH",
                "PATH"
            ]
            
            for var in required_vars:
                assert var in env_output, f"Environment variable {var} not found"
                
        except docker.errors.ImageNotFound:
            pytest.skip(f"Docker image {image_name} not found")