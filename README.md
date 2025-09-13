# Code Learning Path

A comprehensive repository for learning Python programming, containing structured materials, exercises, and resources.

## 🐍 Quick Setup

### Prerequisites
- macOS (Intel or Apple Silicon)
- Terminal access

### 1. Set Up Conda Environment

**Option A: Automated Setup (Recommended)**
```bash
./setup_conda.sh
```

**Option B: Manual Setup**
Follow the detailed guide in [CONDA_SETUP.md](./CONDA_SETUP.md)

### 2. Create Project Environment

After installing Conda:
```bash
# Create a new environment
conda create --name code-learning python=3.9

# Activate the environment
conda activate code-learning

# Install dependencies
pip install -r requirements.txt
```

### 3. Start Learning!

Explore the learning materials in:
- `Pyhton Trajectory/` - Organized learning resources
  - `Books/` - Book-based learning materials
  - `Coursera/` - Course content and exercises
  - `Drills/` - Practice exercises
  - `Websites/` - Web-based tutorials
  - `you tube courses/` - Video course materials

## 📁 Repository Structure

```
code-learning-path/
├── Pyhton Trajectory/          # Main learning materials
│   ├── Books/                  # Book-based content
│   ├── Coursera/              # Online course materials
│   ├── Drills/                # Practice exercises
│   ├── Websites/              # Web tutorials
│   └── you tube courses/      # Video course content
├── CONDA_SETUP.md             # Detailed Conda installation guide
├── GIT_LFS_SETUP.md           # Git Large File Storage guide
├── setup_conda.sh             # Automated Conda setup script
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🔧 Troubleshooting

### Conda Installation Issues

If you encounter `zsh: command not found: conda`:
1. Check the [CONDA_SETUP.md](./CONDA_SETUP.md) guide
2. Ensure you've restarted your terminal
3. Verify initialization: `~/miniconda3/bin/conda init zsh`

### Large File Issues

If you encounter Git errors about large files:
1. Check the [GIT_LFS_SETUP.md](./GIT_LFS_SETUP.md) guide
2. The `.gitignore` already excludes installer files (`.sh`, `.dmg`, etc.)
3. For permanent large files, consider Git LFS

### Common Solutions

**File too large for GitHub:**
```bash
# Option 1: Remove from tracking (recommended for installers)
git rm --cached large-file.sh
git commit -m "Remove large file"

# Option 2: Use Git LFS (for permanent files)
git lfs track "*.sh"
git add .gitattributes large-file.sh
git commit -m "Track with Git LFS"
```

**Conda command not found:**
```bash
# Reinitialize conda
~/miniconda3/bin/conda init zsh
source ~/.zshrc
```

## 📚 Learning Resources

This repository contains materials from various sources:

- **Books**: Python Crash Course and other programming books
- **Online Courses**: Coursera Python specializations
- **Practice**: Coding drills and exercises
- **Video Content**: YouTube course materials
- **Web Tutorials**: FreeCodeCamp and other web resources

## 🚀 Getting Started with Python

1. **Complete Environment Setup** (see above)
2. **Start with Basics**: Explore `Books/Python-Crash-Course-Introduction-To-Programming/`
3. **Practice Regularly**: Use materials in `Drills/`
4. **Take Courses**: Follow structured content in `Coursera/`
5. **Build Projects**: Apply learning through mini-projects

## 🤝 Contributing

This is a personal learning repository. If you're using it as a reference:

1. Fork the repository
2. Create your learning branch
3. Add your own notes and exercises
4. Keep track of your progress

## 📄 License

See [LICENSE](./LICENSE) file for details.

## 🆘 Need Help?

- Review the setup guides: [CONDA_SETUP.md](./CONDA_SETUP.md) and [GIT_LFS_SETUP.md](./GIT_LFS_SETUP.md)
- Check existing course README files in subdirectories
- For Git issues, see the troubleshooting sections above