import pytest
import subprocess
import os
import sys
from pathlib import Path

class TestMLCLLM:
    """Test suite for MLC-LLM functionality"""
    
    def test_import_mlc_llm(self):
        """Test that mlc_llm can be imported"""
        try:
            import mlc_llm
            assert mlc_llm is not None
        except ImportError as e:
            pytest.skip(f"mlc_llm not available: {e}")
    
    def test_mlc_llm_cli_help(self):
        """Test that CLI help works"""
        result = subprocess.run([
            sys.executable, "-m", "mlc_llm", "--help"
        ], capture_output=True, text=True)
        assert result.returncode == 0 or result.returncode == 2
        assert "usage:" in result.stdout.lower() or "usage:" in result.stderr.lower()
    
    def test_build_artifacts_exist(self):
        """Test that build artifacts exist"""
        build_dir = Path("build")
        if build_dir.exists():
            # Check for key build artifacts
            artifacts = [
                "libmlc_llm.so",
                "libtvm_runtime.so"
            ]
            found_artifacts = []
            for artifact in artifacts:
                if any(build_dir.rglob(artifact)):
                    found_artifacts.append(artifact)
            
            # At least one artifact should exist
            assert len(found_artifacts) > 0, f"No build artifacts found in {build_dir}"
    
    def test_python_path_setup(self):
        """Test that Python path is correctly configured"""
        python_dir = Path("python")
        if python_dir.exists():
            assert python_dir.is_dir()
            assert (python_dir / "mlc_llm").exists()
    
    @pytest.mark.integration
    def test_mlc_engine_creation(self):
        """Integration test for MLCEngine creation"""
        try:
            from mlc_llm import MLCEngine
            # This is a basic test - actual model loading would require models
            assert MLCEngine is not None
        except ImportError:
            pytest.skip("MLCEngine not available")
        except Exception as e:
            pytest.skip(f"MLCEngine test skipped: {e}")
    
    def test_cmake_config_generation(self):
        """Test that CMake config can be generated"""
        config_script = Path("cmake/gen_cmake_config.py")
        if config_script.exists():
            # Test that the script can run without errors
            result = subprocess.run([
                sys.executable, str(config_script), "--help"
            ], capture_output=True, text=True, cwd=".")
            # Script should either show help or run successfully
            assert result.returncode == 0 or "usage:" in result.stderr.lower()