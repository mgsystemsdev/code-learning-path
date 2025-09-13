# Git Large File Storage (LFS) Setup

This guide helps you handle large files in Git repositories, specifically for files that exceed GitHub's 100MB limit.

## What is Git LFS?

Git Large File Storage (LFS) is an extension that replaces large files with text pointers inside Git, while storing the actual file contents on a remote server like GitHub.

## When to Use Git LFS

- Files larger than 100MB (GitHub's limit)
- Binary files like images, videos, or installers
- Large datasets or model files
- Any file that causes `remote rejected` errors due to size

## Installation

### macOS (using Homebrew)

```bash
# Install Git LFS
brew install git-lfs

# Initialize Git LFS in your repository
git lfs install
```

### Alternative Installation Methods

```bash
# Using curl (if Homebrew isn't available)
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
sudo apt-get install git-lfs

# Or download from GitHub releases
# Visit: https://github.com/git-lfs/git-lfs/releases
```

## Usage

### For Existing Large Files (Already Committed)

If you have a large file that's already been committed and is causing push errors:

1. **Track the file with Git LFS:**
   ```bash
   git lfs track "filename.sh"
   # or use patterns
   git lfs track "*.sh"
   git lfs track "*.dmg"
   ```

2. **Add the .gitattributes file:**
   ```bash
   git add .gitattributes
   ```

3. **Re-add the large file:**
   ```bash
   git add filename.sh
   git commit -m "Track large file with Git LFS"
   ```

4. **Push changes:**
   ```bash
   git push
   ```

### For New Large Files

1. **Track file types before adding them:**
   ```bash
   git lfs track "*.sh"
   git lfs track "*.dmg"
   git lfs track "*.pkg"
   ```

2. **Add and commit normally:**
   ```bash
   git add .gitattributes
   git add your-large-file.sh
   git commit -m "Add large file with LFS"
   git push
   ```

## Common Scenarios

### Scenario 1: Miniconda Installer Error

**Problem:**
```
error: File Miniconda3-latest-MacOSX-arm64.sh is 199.94 MB; 
this exceeds GitHub's file size limit of 100.00 MB
```

**Solution Option 1 - Use Git LFS:**
```bash
# Install and initialize Git LFS
brew install git-lfs
git lfs install

# Track the installer file
git lfs track "Miniconda3-latest-MacOSX-*.sh"

# Commit the changes
git add .gitattributes
git add Miniconda3-latest-MacOSX-*.sh
git commit -m "Track Miniconda installer with Git LFS"
git push
```

**Solution Option 2 - Remove from Repository:**
```bash
# Remove the file from Git (but keep locally)
git rm --cached Miniconda3-latest-MacOSX-*.sh

# Commit the removal
git commit -m "Remove large installer file"
git push
```

### Scenario 2: Multiple Large Files

```bash
# Track multiple file types at once
git lfs track "*.dmg" "*.pkg" "*.zip" "*.tar.gz" "*.sh"

# Check what's being tracked
git lfs ls-files

# See tracking patterns
cat .gitattributes
```

## Verification Commands

```bash
# Check LFS status
git lfs status

# List LFS files
git lfs ls-files

# Show LFS tracking patterns
git lfs track

# Check LFS file info
git lfs pointer --file=your-large-file.sh
```

## Best Practices

1. **Add to .gitignore first:** For temporary/build files
   ```bash
   # Add to .gitignore
   *.sh
   *.dmg
   *.pkg
   ```

2. **Use LFS for permanent large files:** Documentation, datasets, models

3. **Track patterns, not individual files:**
   ```bash
   git lfs track "*.model"
   git lfs track "data/**"
   ```

4. **Clean up after installation:** Remove temporary installers
   ```bash
   rm Miniconda3-latest-MacOSX-*.sh
   ```

## Troubleshooting

### Issue: LFS files not uploading

**Check authentication:**
```bash
git config --global credential.helper store
git lfs env
```

### Issue: Files still rejected after LFS setup

**Check if properly tracked:**
```bash
git lfs ls-files
cat .gitattributes
```

### Issue: Need to remove LFS tracking

```bash
git lfs untrack "*.sh"
git add .gitattributes
git commit -m "Stop tracking .sh files with LFS"
```

## For This Repository

The `.gitignore` file already excludes `.sh` files, which is the recommended approach for installer scripts. You should:

1. Download installers temporarily
2. Run the installation
3. Remove the installer files
4. Let `.gitignore` prevent accidental commits

Only use Git LFS if you specifically need to store large files permanently in the repository.