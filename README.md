# MLC-LLM DevOps Solution

[![CI/CD Pipeline](https://github.com/jaymineh/mlc-llm/actions/workflows/pipeline.yml/badge.svg)](https://github.com/jaymineh/mlc-llm/actions/workflows/pipeline.yml)
[![Docker Image](https://ghcr.io/jaymineh/mlc-llm:latest)](https://ghcr.io/jaymineh/mlc-llm)

Production-quality DevOps workflow for [MLC-LLM](https://github.com/mlc-ai/mlc-llm) with automated testing, cross-platform builds, and container orchestration.

## 🚀 Quick Start

### Prerequisites

- Docker 20.10+
- Git with LFS support
- GitHub account with GHCR access

### Using Docker (Recommended)

```bash
# Pull the latest image
docker pull ghcr.io/your-org/mlc-llm:latest

# Run in development mode
docker run -it --rm -v $(pwd):/workspace ghcr.io/your-org/mlc-llm:dev

# Run in production mode
docker run --rm ghcr.io/your-org/mlc-llm:latest chat --help
```

### Local Development

```bash
# Clone repository
git clone --recursive https://github.com/your-org/mlc-llm.git
cd mlc-llm

# Build Docker image
docker build -t mlc-llm:local .

# Run tests
docker run --rm -v $(pwd):/workspace mlc-llm:local python -m pytest
```

## 🏗️ Architecture

### Docker Multi-Stage Build

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Base Image    │───▶│  Development    │    │     Builder     │
│   Dependencies  │    │   Environment   │    │   Environment   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                               ┌─────────────────┐
                                               │     Runtime     │
                                               │   Environment   │
                                               └─────────────────┘
```

### CI/CD Pipeline Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    Test     │───▶│Docker Build │───▶│Cross-Platform│───▶│   Release   │
│   Stage     │    │   & Push    │    │    Build    │    │  Creation   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                    │                    │                │
   ┌────▼────┐          ┌───▼───┐           ┌────▼────┐      ┌────▼────┐
   │ Lint    │          │ GHCR  │           │ Linux   │      │ GitHub  │
   │ Format  │          │ Push  │           │ Windows │      │Release  │
   │ Test    │          │       │           │ Builds  │      │         │
   └─────────┘          └───────┘           └─────────┘      └─────────┘
```

## 🐳 Docker Usage

### Development Environment

The Docker image serves dual purposes:

**Interactive Development:**
```bash
docker run -it --rm \
  -v $(pwd):/workspace \
  -w /workspace \
  mlc-llm:dev bash
```

**Build Environment:**
```bash
docker run --rm \
  -v $(pwd):/workspace \
  -w /workspace \
  mlc-llm:runtime \
  python -m mlc_llm compile --help
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MLC_LLM_SOURCE_DIR` | Source directory path | `/app` |
| `PYTHONPATH` | Python module search path | `/app/python:$PYTHONPATH` |

## 🔧 Development Workflow

### 1. Local Development Setup

```bash
# Create development environment
docker run -it --rm \
  -v $(pwd):/workspace \
  -p 8888:8888 \
  mlc-llm:dev

# Inside container
conda activate mlc-chat-venv
jupyter lab --ip=0.0.0.0 --allow-root
```

### 2. Running Tests

```bash
# Unit tests
pytest tests/ -v

# Integration tests
pytest tests/ -m integration

# Docker tests
pytest tests/ -m docker
```

### 3. Building from Source

```bash
# Configure build
mkdir -p build && cd build
python ../cmake/gen_cmake_config.py

# Build
cmake ..
cmake --build . --parallel $(nproc)
```

## 🚀 CI/CD Pipeline

### Triggers

- **Push to main/develop**: Full pipeline
- **Pull Request**: Test and build
- **Release**: Full pipeline + deployment

### Jobs Overview

1. **Test Job**: Linting, formatting, unit tests
2. **Docker Build**: Multi-arch container build
3. **Cross-Platform Build**: Linux/Windows wheels
4. **Release**: GitHub release creation

### Secrets Required

| Secret | Description |
|--------|-------------|
| `GITHUB_TOKEN` | Automatic GitHub token for GHCR |

## 📦 Releases

Releases are automatically created when:
- A new tag is pushed matching `v*.*.*` pattern
- GitHub release is published

### Artifacts

- Python wheels for Linux x64
- Python wheels for Windows x64  
- Docker images in GHCR

## 🛠️ Build Dependencies

### System Requirements

- CMake >= 3.24
- Git with LFS
- Rust and Cargo
- Python 3.9-3.11
- C++ compiler with C++17 support

### GPU Support

| Platform | Runtime | Requirements |
|----------|---------|--------------|
| NVIDIA | CUDA >= 11.8 | CUDA Toolkit |
| AMD | ROCm | ROCm Toolkit |
| Apple | Metal | macOS 10.15+ |
| Intel | Vulkan | Vulkan drivers |

## 🐛 Troubleshooting

### Common Issues

**Docker build fails:**
```bash
# Check Docker daemon
docker info

# Clean build cache
docker builder prune

# Build with verbose output
docker build --progress=plain .
```

**Tests fail:**
```bash
# Run specific test
pytest tests/test_mlc_llm.py::TestMLCLLM::test_import_mlc_llm -v

# Skip integration tests
pytest -m "not integration"
```

**Import errors:**
```bash
# Check Python path
echo $PYTHONPATH

# Verify installation
python -c "import mlc_llm; print(mlc_llm.__file__)"
```

## 📚 Additional Resources

- [MLC-LLM Documentation](https://llm.mlc.ai/docs/)
- [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.