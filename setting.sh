#!/bin/bash

# Exit script if any command fails
set -e

# Step 1: Clone the repository from GitHub
echo "Cloning repository from GitHub..."
git clone <GITHUB_REPO_URL> project
cd project

# Step 2: Download and install Miniconda
echo "Downloading and installing Miniconda..."
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"

# Initialize Conda (only needed if this is the first time)
echo "Initializing Conda..."
conda init
source ~/.bashrc

# Step 3: Create a Conda environment and install requirements
echo "Setting up Conda environment and installing requirements..."
conda create -n myenv python=3.10 -y
conda activate myenv
conda install --file requirements.txt -y

# Step 4: Run the Python code
echo "Running Python code..."
python main.py