# Setting Up Conda on macOS

This guide helps you install and configure Conda (Miniconda) on your macOS system.

## Prerequisites

- macOS system (Intel or Apple Silicon M1/M2/M3)
- Terminal access
- Internet connection

## Installation Steps

### 1. Determine Your Mac Architecture

First, check if you have an Intel or Apple Silicon Mac:

```bash
uname -m
```

- `arm64` = Apple Silicon (M1/M2/M3)
- `x86_64` = Intel

### 2. Download and Install Miniconda

#### For Apple Silicon (M1/M2/M3) Macs:

```bash
# Download Miniconda for Apple Silicon
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh

# Run the installer
bash Miniconda3-latest-MacOSX-arm64.sh
```

#### For Intel Macs:

```bash
# Download Miniconda for Intel
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh

# Run the installer
bash Miniconda3-latest-MacOSX-x86_64.sh
```

### 3. Follow Installation Prompts

1. Press `Enter` to review the license agreement
2. Press `Space` to scroll through the license
3. Type `yes` to accept the license
4. Press `Enter` to confirm the installation location (default is recommended)
5. Type `yes` when asked to initialize Miniconda3

### 4. Initialize Conda for Your Shell

```bash
# Initialize conda for zsh (default shell on newer macOS)
~/miniconda3/bin/conda init zsh

# For bash users (if you're using bash instead of zsh)
~/miniconda3/bin/conda init bash
```

### 5. Restart Your Terminal

Close and reopen your terminal, or run:

```bash
source ~/.zshrc  # For zsh users
# or
source ~/.bashrc  # For bash users
```

### 6. Verify Installation

```bash
# Check conda version
conda --version

# List available environments
conda env list

# Check if base environment is active
conda info
```

## Common Issues and Solutions

### Issue: `zsh: command not found: conda`

**Solution:**
1. Make sure you completed step 4 (initialization)
2. Restart your terminal
3. If still not working, manually add to PATH:
   ```bash
   echo 'export PATH="$HOME/miniconda3/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```

### Issue: Permission Denied

**Solution:**
- Make sure the installer script has execute permissions:
  ```bash
  chmod +x Miniconda3-latest-MacOSX-*.sh
  ```

## Basic Conda Commands

```bash
# Create a new environment
conda create --name myenv python=3.9

# Activate an environment
conda activate myenv

# Install packages
conda install package_name

# List installed packages
conda list

# Deactivate environment
conda deactivate

# Remove an environment
conda env remove --name myenv
```

## Using with This Repository

After installing Conda, you can create an environment for this project:

```bash
# Create environment from requirements.txt
conda create --name code-learning python=3.9
conda activate code-learning
pip install -r requirements.txt
```

## Cleanup

After installation, you can safely remove the installer file:

```bash
rm Miniconda3-latest-MacOSX-*.sh
```

**Note:** The installer files are already excluded from Git tracking via `.gitignore`.