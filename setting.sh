#!/bin/bash
<<<<<<< HEAD
# chmod +x setting.sh
=======

>>>>>>> 293afdb (add requiemnet files and sh file)
# Exit script if any command fails
set -e

# Step 1: Clone the repository from GitHub
<<<<<<< HEAD
# echo "Cloning repository from GitHub..."
# git clone <GITHUB_REPO_URL> project
# cd project
=======
echo "Cloning repository from GitHub..."
git clone <GITHUB_REPO_URL> project
cd project
>>>>>>> 293afdb (add requiemnet files and sh file)

# Step 2: Download and install Miniconda
echo "Downloading and installing Miniconda..."
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"

<<<<<<< HEAD

git config --global user.name "NgocDung211"
git config --global user.email "ngocdug21103@gmail.com"
curl -fsSL https://ollama.com/install.sh | sh
ollama pull mantis_lego696/phogpt_q4_k_m

=======
>>>>>>> 293afdb (add requiemnet files and sh file)
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
<<<<<<< HEAD
# echo "Running Python code..."
# python main.py
=======
echo "Running Python code..."
python main.py
>>>>>>> 293afdb (add requiemnet files and sh file)
