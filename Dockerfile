# Multi-stage Dockerfile for MLC-LLM
# Stage 1: Base image with dependencies
FROM continuumio/miniconda3:latest AS base

# Create non-root user
RUN groupadd -r mlcuser && useradd -r -g mlcuser -m -s /bin/bash mlcuser

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    curl \
    wget \
    ninja-build \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Create conda environment
RUN conda create -n mlc-chat-venv -c conda-forge \
    "cmake>=3.24" \
    rust \
    git \
    python=3.11 \
    && conda clean -afy

# Stage 2: Development environment
FROM base AS development

# Set working directory
WORKDIR /workspace

# Switch to non-root user
USER mlcuser

# Copy conda environment
COPY --from=base --chown=mlcuser:mlcuser /opt/conda /opt/conda

# Make conda available
ENV PATH="/opt/conda/bin:$PATH"

# Install development tools
RUN conda install -n mlc-chat-venv -c conda-forge \
    jupyter \
    ipython \
    pytest \
    black \
    flake8 \
    mypy \
    && conda clean -afy

# Set up shell
SHELL ["/bin/bash", "-c"]

# Default command for development
CMD ["bash"]

# Stage 3: Build environment
FROM base AS builder

# Set working directory
WORKDIR /build
RUN chown -R mlcuser:mlcuser /build

# Switch to non-root user
USER mlcuser

# Copy source code
COPY --chown=mlcuser:mlcuser . .

# Make conda available
ENV PATH="/opt/conda/bin:$PATH"

SHELL ["/bin/bash", "-c"]

CMD ["bash"]

# Activate conda environment and build
RUN source /opt/conda/etc/profile.d/conda.sh && \
    conda activate mlc-chat-venv && \
    mkdir -p build && cd build && \
    python -m pip install --pre -U -f https://mlc.ai/wheels mlc-ai-nightly-cpu && \
    python ../cmake/gen_cmake_config.py && \
    cmake .. && \
    cmake --build . --parallel $(nproc)

# Stage 4: Final runtime image
FROM base AS runtime

# Set working directory
WORKDIR /app

# Switch to non-root user
USER mlcuser

# Copy built artifacts
COPY --from=builder --chown=mlcuser:mlcuser /build/build ./build
COPY --from=builder --chown=mlcuser:mlcuser /build/python ./python

# Make conda available
ENV PATH="/opt/conda/bin:$PATH"

# Set environment variables
ENV MLC_LLM_SOURCE_DIR="/app"
ENV PYTHONPATH="/app/python:$PYTHONPATH"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD conda run -n mlc-chat-venv python -c "import mlc_llm; print('OK')" || exit 1

# Default entrypoint
ENTRYPOINT ["conda", "run", "-n", "mlc-chat-venv", "python", "-m", "mlc_llm"]