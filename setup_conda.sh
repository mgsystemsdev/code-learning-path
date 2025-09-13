#!/bin/bash

# Conda Setup Script for macOS
# This script automates the installation of Miniconda on macOS

set -e  # Exit on any error

echo "🐍 Conda Setup Script for macOS"
echo "================================"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to detect architecture
detect_arch() {
    local arch=$(uname -m)
    if [[ "$arch" == "arm64" ]]; then
        echo "arm64"
    elif [[ "$arch" == "x86_64" ]]; then
        echo "x86_64"
    else
        echo "unknown"
    fi
}

# Function to cleanup installer files
cleanup() {
    echo "🧹 Cleaning up installer files..."
    rm -f Miniconda3-latest-MacOSX-*.sh
    echo "✅ Cleanup complete"
}

# Check if conda is already installed
if command_exists conda; then
    echo "✅ Conda is already installed!"
    conda --version
    echo ""
    echo "To create a new environment for this project:"
    echo "  conda create --name code-learning python=3.9"
    echo "  conda activate code-learning"
    echo "  pip install -r requirements.txt"
    exit 0
fi

echo "❌ Conda not found. Installing Miniconda..."

# Detect architecture
ARCH=$(detect_arch)
echo "🔍 Detected architecture: $ARCH"

if [[ "$ARCH" == "unknown" ]]; then
    echo "❌ Unsupported architecture. This script supports Intel (x86_64) and Apple Silicon (arm64) Macs only."
    exit 1
fi

# Set installer filename based on architecture
if [[ "$ARCH" == "arm64" ]]; then
    INSTALLER="Miniconda3-latest-MacOSX-arm64.sh"
    DOWNLOAD_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh"
    echo "📱 Installing for Apple Silicon (M1/M2/M3)"
else
    INSTALLER="Miniconda3-latest-MacOSX-x86_64.sh"
    DOWNLOAD_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh"
    echo "💻 Installing for Intel Mac"
fi

# Download installer if it doesn't exist
if [[ ! -f "$INSTALLER" ]]; then
    echo "⬇️  Downloading Miniconda installer..."
    if command_exists curl; then
        curl -O "$DOWNLOAD_URL"
    elif command_exists wget; then
        wget "$DOWNLOAD_URL"
    else
        echo "❌ Neither curl nor wget found. Please install one of them first."
        exit 1
    fi
    echo "✅ Download complete"
else
    echo "✅ Installer already exists: $INSTALLER"
fi

# Make installer executable
chmod +x "$INSTALLER"

echo ""
echo "🚀 Running Miniconda installer..."
echo "   Please follow the prompts:"
echo "   1. Press ENTER to review the license"
echo "   2. Press SPACE to scroll, 'q' to finish reading"
echo "   3. Type 'yes' to accept the license"
echo "   4. Press ENTER to accept default location"
echo "   5. Type 'yes' to initialize conda"
echo ""

# Run installer
bash "$INSTALLER"

# Check if installation was successful
if [[ $? -eq 0 ]]; then
    echo ""
    echo "✅ Miniconda installation completed!"
    
    # Initialize conda for the current shell
    echo "🔧 Initializing conda for your shell..."
    
    # Detect shell and initialize accordingly
    if [[ "$SHELL" == *"zsh"* ]]; then
        ~/miniconda3/bin/conda init zsh
        echo "🐚 Initialized for zsh"
    elif [[ "$SHELL" == *"bash"* ]]; then
        ~/miniconda3/bin/conda init bash
        echo "🐚 Initialized for bash"
    else
        echo "⚠️  Unknown shell: $SHELL"
        echo "   Please run manually: ~/miniconda3/bin/conda init $(basename $SHELL)"
    fi
    
    echo ""
    echo "🎉 Setup complete! Please restart your terminal or run:"
    if [[ "$SHELL" == *"zsh"* ]]; then
        echo "   source ~/.zshrc"
    else
        echo "   source ~/.bashrc"
    fi
    echo ""
    echo "Then verify installation with:"
    echo "   conda --version"
    echo ""
    echo "To create an environment for this project:"
    echo "   conda create --name code-learning python=3.9"
    echo "   conda activate code-learning"
    echo "   pip install -r requirements.txt"
    
    # Cleanup installer
    cleanup
    
else
    echo "❌ Installation failed. Please check the error messages above."
    exit 1
fi