# Development Guide

## 🏗️ Local Development Setup

### Method 1: Docker Development Environment

```bash
# Build development image
docker build --target development -t mlc-llm:dev .

# Run interactive development container
docker run -it --rm \
  -v $(pwd):/workspace \
  -v ~/.gitconfig:/home/mlcuser/.gitconfig:ro \
  -p 8888:8888 \
  mlc-llm:dev

# Inside container
conda activate mlc-chat-venv
```

### Method 2: Local Conda Environment

```bash
# Create conda environment
conda create -n mlc-chat-venv -c conda-forge \
  "cmake>=3.24" \
  rust \
  git \
  python=3.11

# Activate environment
conda activate mlc-chat-venv

# Clone repository
git clone --recursive https://github.com/mlc-ai/mlc-llm.git
cd mlc-llm

# Build from source
mkdir -p build && cd build
python ../cmake/gen_cmake_config.py
cmake ..
cmake --build . --parallel $(nproc)
cd ..

# Install as Python package
export MLC_LLM_SOURCE_DIR=$(pwd)
export PYTHONPATH=$MLC_LLM_SOURCE_DIR/python:$PYTHONPATH
```

## 🧪 Testing Strategy

### Test Categories

1. **Unit Tests**: Individual component testing
2. **Integration Tests**: End-to-end functionality
3. **Docker Tests**: Container functionality
4. **Performance Tests**: Benchmarking (optional)

### Running Tests

```bash
# All tests
pytest

# Specific test category
pytest -m "not slow"
pytest -m integration
pytest -m docker

# With coverage
pytest --cov=mlc_llm --cov-report=html

# Parallel execution
pytest -n auto
```

### Writing Tests

```python
import pytest
from mlc_llm import MLCEngine

class TestNewFeature:
    """Test new feature implementation"""
    
    def test_basic_functionality(self):
        """Test basic functionality"""
        # Arrange
        expected = "expected_result"
        
        # Act
        result = your_function()
        
        # Assert
        assert result == expected
    
    @pytest.mark.integration
    def test_integration_scenario(self):
        """Test integration scenario"""
        # Integration test implementation
        pass
    
    @pytest.mark.slow
    def test_performance_scenario(self):
        """Test performance scenario"""
        # Performance test implementation
        pass
```

## 🔧 Development Workflow

### 1. Feature Development

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes
# ... development work ...

# Run tests
pytest tests/

# Format code
black .
flake8 .

# Commit changes
git add .
git commit -m "feat: add new feature"

# Push branch
git push origin feature/new-feature
```

### 2. Code Quality

**Formatting:**
```bash
# Format Python code
black .

# Sort imports
isort .

# Lint code
flake8 .
```

**Type Checking:**
```bash
# Type check
mypy . --ignore-missing-imports
```

### 3. Docker Development

**Building Images:**
```bash
# Build development image
docker build --target development -t mlc-llm:dev .

# Build runtime image
docker build --target runtime -t mlc-llm:runtime .

# Build all stages
docker build -t mlc-llm:latest .
```

**Testing Docker:**
```bash
# Test development environment
docker run -it --rm mlc-llm:dev python --version

# Test runtime environment
docker run --rm mlc-llm:runtime python -c "import mlc_llm"

# Test with mounted source
docker run -it --rm -v $(pwd):/workspace mlc-llm:dev
```

## 📋 Development Environment Features

### Jupyter Lab Integration

```bash
# Start Jupyter Lab in container
docker run -it --rm \
  -v $(pwd):/workspace \
  -p 8888:8888 \
  mlc-llm:dev \
  conda run -n mlc-chat-venv jupyter lab --ip=0.0.0.0 --allow-root
```

### VS Code Integration

**.devcontainer/devcontainer.json:**
```json
{
  "name": "MLC-LLM Development",
  "dockerFile": "../Dockerfile",
  "target": "development",
  "mounts": [
    "source=${localWorkspaceFolder},target=/workspace,type=bind"
  ],
  "workspaceFolder": "/workspace",
  "remoteUser": "mlcuser",
  "postCreateCommand": "conda activate mlc-chat-venv",
  "extensions": [
    "ms-python.python",
    "ms-python.black-formatter",
    "ms-python.flake8"
  ]
}
```

### Git Hooks

**pre-commit configuration (.pre-commit-config.yaml):**
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black
  
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
  
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
```

## 🚀 Performance Optimization

### Build Optimization

```bash
# Parallel build
cmake --build . --parallel $(nproc)

# Release build
cmake -DCMAKE_BUILD_TYPE=Release ..

# Use Ninja generator
cmake -GNinja ..
ninja
```

### Container Optimization

```dockerfile
# Multi-stage build
FROM base AS builder
# ... build steps ...

FROM runtime AS final
COPY --from=builder /build/artifacts /app/
```

## 🔍 Debugging

### Debug Build

```bash
# Debug build
cmake -DCMAKE_BUILD_TYPE=Debug ..
cmake --build .

# With debug symbols
cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo ..
cmake --build .
```

### Container Debugging

```bash
# Debug container startup
docker run -it --rm --entrypoint=/bin/bash mlc-llm:runtime

# Inspect container
docker inspect mlc-llm:runtime

# Check logs
docker logs 
```

### Python Debugging

```python
# Using debugger
import pdb; pdb.set_trace()

# Using rich traceback
from rich.traceback import install
install()
```

## 📊 Monitoring and Profiling

### Performance Monitoring

```python
import time
import cProfile

# Time measurement
start_time = time.time()
# ... your code ...
end_time = time.time()
print(f"Execution time: {end_time - start_time:.2f}s")

# Profiling
cProfile.run('your_function()')
```

### Memory Profiling

```bash
# Install memory profiler
pip install memory-profiler

# Profile memory usage
python -m memory_profiler your_script.py
```

## 🤝 Contributing Guidelines

### Code Style

- Follow PEP 8
- Use Black for formatting
- Maximum line length: 88 characters
- Use type hints where appropriate

### Commit Messages

```
feat: add new feature
fix: resolve bug in component
docs: update documentation
style: format code
refactor: restructure module
test: add test cases
chore: update dependencies
```

### Pull Request Process

1. Fork repository
2. Create feature branch
3. Implement changes
4. Add tests
5. Update documentation
6. Submit pull request
7. Address review feedback
8. Merge after approval

## 📚 Additional Resources

- [Python Development Best Practices](https://docs.python-guide.org/)