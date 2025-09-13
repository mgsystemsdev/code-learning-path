#!/bin/bash

# Setup Verification Script
# Checks if Conda and other tools are properly installed

echo "🔍 Verifying Development Environment Setup"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check command and report status
check_command() {
    local cmd="$1"
    local name="$2"
    local install_hint="$3"
    
    if command -v "$cmd" >/dev/null 2>&1; then
        local version=$($cmd --version 2>/dev/null | head -n1)
        echo -e "✅ ${GREEN}$name${NC}: $version"
        return 0
    else
        echo -e "❌ ${RED}$name${NC}: Not found"
        if [[ -n "$install_hint" ]]; then
            echo -e "   ${YELLOW}💡 $install_hint${NC}"
        fi
        return 1
    fi
}

# Function to check Python packages
check_python_package() {
    local package="$1"
    local name="$2"
    
    if python -c "import $package" 2>/dev/null; then
        local version=$(python -c "import $package; print($package.__version__)" 2>/dev/null)
        echo -e "✅ ${GREEN}$name${NC}: $version"
        return 0
    else
        echo -e "❌ ${RED}$name${NC}: Not installed"
        return 1
    fi
}

echo ""
echo "🐍 Python Environment:"
echo "---------------------"

# Check Python
check_command python "Python" "Install with: conda install python"
if command -v python >/dev/null 2>&1; then
    python_version=$(python --version 2>&1)
    echo "   Location: $(which python)"
    
    # Check if we're in a conda environment
    if [[ -n "$CONDA_DEFAULT_ENV" ]]; then
        echo -e "   ${GREEN}Active conda environment: $CONDA_DEFAULT_ENV${NC}"
    else
        echo -e "   ${YELLOW}No active conda environment${NC}"
    fi
fi

echo ""
echo "📦 Package Manager:"
echo "------------------"

# Check Conda
check_command conda "Conda" "Run: ./setup_conda.sh"
if command -v conda >/dev/null 2>&1; then
    echo "   Location: $(which conda)"
    echo "   Available environments:"
    conda env list | grep -v "^#" | sed 's/^/     /'
fi

# Check pip
check_command pip "pip" "Usually comes with Python"

echo ""
echo "🔧 Development Tools:"
echo "--------------------"

# Check Git
check_command git "Git" "Install with: brew install git"

# Check Git LFS
check_command git-lfs "Git LFS" "Install with: brew install git-lfs"

# Check curl
check_command curl "curl" "Usually pre-installed on macOS"

echo ""
echo "📚 Project Dependencies:"
echo "----------------------"

# Check if requirements.txt exists and verify packages
if [[ -f "requirements.txt" ]]; then
    echo "✅ requirements.txt found"
    
    # If Python is available, check some key packages
    if command -v python >/dev/null 2>&1; then
        check_python_package "pandas" "pandas"
        check_python_package "numpy" "numpy" 
        check_python_package "streamlit" "streamlit"
    fi
else
    echo -e "❌ ${RED}requirements.txt${NC}: Not found"
fi

echo ""
echo "📁 Project Structure:"
echo "-------------------"

# Check key directories
directories=("Pyhton Trajectory " "CONDA_SETUP.md" "GIT_LFS_SETUP.md" "setup_conda.sh")
for item in "${directories[@]}"; do
    if [[ -e "$item" ]]; then
        echo -e "✅ ${GREEN}$item${NC}: Found"
    else
        echo -e "❌ ${RED}$item${NC}: Missing"
    fi
done

echo ""
echo "🎯 Next Steps:"
echo "-------------"

if ! command -v conda >/dev/null 2>&1; then
    echo "1. Install Conda: ./setup_conda.sh"
fi

if [[ -z "$CONDA_DEFAULT_ENV" ]] || [[ "$CONDA_DEFAULT_ENV" == "base" ]]; then
    echo "2. Create project environment:"
    echo "   conda create --name code-learning python=3.9"
    echo "   conda activate code-learning"
fi

if [[ -f "requirements.txt" ]]; then
    echo "3. Install project dependencies:"
    echo "   pip install -r requirements.txt"
fi

echo "4. Start learning! Explore the 'Pyhton Trajectory ' directory"

echo ""
echo "🆘 Need Help?"
echo "   • Read CONDA_SETUP.md for detailed installation instructions"
echo "   • Read GIT_LFS_SETUP.md for handling large files"
echo "   • Check README.md for project overview"