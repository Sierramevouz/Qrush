# Step 1: Use a development image to get build tools like nvcc and system libraries
FROM nvidia/cuda:11.8.0-devel-ubuntu20.04

# Step 2: Set non-interactive mode for package installation to prevent prompts
ENV DEBIAN_FRONTEND=noninteractive

# Step 3: Install system-level core dependencies, including Python 3.11 from the deadsnakes PPA
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    software-properties-common \
    build-essential git cmake \
    libomp-dev \
    curl \
    && add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    python3.11 \
    python3.11-dev \
    python3.11-distutils \
    && rm -rf /var/lib/apt/lists/*

# Step 4: Set python3.11 as default AND correctly install pip for it
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1 && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 && \
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python get-pip.py && \
    rm get-pip.py && \
    python -m pip install --no-cache-dir --upgrade pip

# Step 5: Install all Python dependencies, including fixes for DGL and NumPy
# 5a: Install PyTorch for CUDA 11.8
RUN python -m pip install --no-cache-dir \
    'torch==2.1.0+cu118' \
    'torchvision==0.16.0+cu118' \
    'torchaudio==2.1.0+cu118' \
    --index-url https://download.pytorch.org/whl/cu118

# 5b: Install DGL using the correct find-links option
RUN python -m pip install --no-cache-dir dgl \
    -f https://data.dgl.ai/wheels/cu118/repo.html

# 5c: Install other packages, including all discovered dependencies for DGL and Quartz
RUN python -m pip install --no-cache-dir \
    'numpy<2.0' \
    'torchdata==0.7.0' \
    'pandas' \
    'pydantic' \
    'pybind11' \
    'networkx==3.1' \
    'matplotlib' \
    'tqdm' \
    'scipy' \
    'scikit-learn' \
    'pyyaml' \
    'qiskit' \
    'cython'

# Step 6: Set up the workspace
WORKDIR /workspace

# Step 7: Clone Quartz and its submodules
RUN git clone --recursive https://github.com/quantum-compiler/quartz.git

# Step 8: Build and install Quartz C++ core library
RUN cd quartz && \
    mkdir build && \
    cd build && \
    cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local/quartz -DPYTHON_EXECUTABLE=/usr/bin/python3.11 && \
    make -j$(nproc) && \
    make install

# Step 9: Install the Quartz Python package, pointing to our local installation
RUN cd quartz/python && \
    sed -i "s|'/usr/local/include/'|'/usr/local/quartz/include'|g" setup.py && \
    sed -i "s|'/usr/local/lib/'|'/usr/local/quartz/lib'|g" setup.py && \
    pip install -e .

# Step 10: Set the library path so Python can find libquartz_runtime.so at runtime
ENV LD_LIBRARY_PATH=/usr/local/quartz/lib:$LD_LIBRARY_PATH

# Step 11: Set the final working directory
WORKDIR /workspace

# Step 12: Start a bash shell by default when the container runs
CMD ["/bin/bash"]