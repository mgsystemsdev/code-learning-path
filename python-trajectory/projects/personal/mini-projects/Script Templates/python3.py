# ============================================================
#  Python Script: Generate Folder Structure for Coursera Course
#  Author:        Miguel Gonzalez Almonte
#  Purpose:       Automatically create folders and module files
#                 with headers for each class in your course.
# ============================================================

from pathlib import Path          # Lets us work with folders and paths easily
from datetime import date         # Lets us get today’s date

# ------------------------------------------------------------
# Step 1: Define where to create the course folders
# This will use your Documents folder automatically
# ------------------------------------------------------------
base_dir = Path.home() / "Documents" / "Python class" / "Python3 Coursera Class"

# ------------------------------------------------------------
# Step 2: Define your info for the headers
# ------------------------------------------------------------
author = "Miguel Gonzalez Almonte"             # Your name
created = date.today().strftime("%Y-%m-%d")    # Today's date like '2025-06-01'

# ------------------------------------------------------------
# Step 3: Define how many modules each class has
# ------------------------------------------------------------
course_structure = {
    "class1": 4,
    "class2": 5,
    "class3": 4,
    "class4": 4,
    "class5": 3
}

# ------------------------------------------------------------
# Step 4: Create the header text for each file
# This is a reusable function — just give it class/module numbers
# ------------------------------------------------------------
def generate_header(class_num, module_num):
    return f"""# ============================================================
#  File:        module{module_num}.py
#  Author:      {author}
#  Created:     {created}
#  Description: 
# ------------------------------------------------------------
#  Course:      Python 3 Programming Specialization (Coursera)
#  Module:      Module {module_num} of Class {class_num}
#  Purpose:     
# ------------------------------------------------------------
#  Notes:
#  - 
#  - 
#  - 
# ============================================================
"""

# ------------------------------------------------------------
# Step 5: Create folders and module files
# ------------------------------------------------------------
for class_name, num_modules in course_structure.items():
    class_path = base_dir / class_name              # e.g., ~/Documents/CourseraPython/class1
    class_path.mkdir(parents=True, exist_ok=True)   # Make the folder (no error if it exists)

    for i in range(1, num_modules + 1):             # Loop through module1, module2, ...
        file_path = class_path / f"module{i}.py"    # Build the file path
        with file_path.open("w") as f:              # Open the file for writing
            f.write(generate_header(class_name[-1], i))  # Write the header inside

# ------------------------------------------------------------
# Step 6: Done! Let the user know where files went
# ------------------------------------------------------------
print(f"✅ Files created inside: {base_dir}")
