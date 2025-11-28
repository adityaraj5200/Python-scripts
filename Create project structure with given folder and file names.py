# Frontend:


import os

def create_file(path):
    """Helper function to create an empty file."""
    with open(path, "w") as f:
        pass


def create_structure(root_path):
    """
    Creates the full project structure for frontend.
    root_path must be the path where 'frontend/' should be created.
    Example: root_path = r"C:/Users/Aditya/Desktop"
    """

    # ===========================
    # Directory Structure
    # ===========================
    directories = [
        "frontend/public/content",
        "frontend/public/assets",
        "frontend/src",
        "frontend/src/lib",
        "frontend/src/hooks",
        "frontend/src/components/layout",
        "frontend/src/components/hero",
        "frontend/src/components/about",
        "frontend/src/components/ui",
        "frontend/src/components/skills",
        "frontend/src/components/experience",
        "frontend/src/components/projects",
        "frontend/src/components/contact",
        "frontend/src/animations",
    ]

    # ===========================
    # File Structure
    # ===========================
    files = [
        # public/content json files
        "frontend/public/content/about.json",
        "frontend/public/content/skills.json",
        "frontend/public/content/experience.json",
        "frontend/public/content/projects.json",
        "frontend/public/content/education.json",
        "frontend/public/content/contact.json",

        # public assets
        "frontend/public/assets/photo.jpg",
        "frontend/public/assets/arch-url-shortener.svg",
        "frontend/public/assets/arch-ecommerce.svg",
        "frontend/public/assets/logo.svg",

        # public root files
        "frontend/public/favicon.ico",
        "frontend/public/index.html",

        # src root
        "frontend/src/App.jsx",
        "frontend/src/main.jsx",
        "frontend/src/index.css",

        # lib
        "frontend/src/lib/fetchContent.js",

        # hooks
        "frontend/src/hooks/usePrefersReducedMotion.js",

        # components/layout
        "frontend/src/components/layout/Navbar.jsx",
        "frontend/src/components/layout/Footer.jsx",

        # hero
        "frontend/src/components/hero/Hero.jsx",

        # about
        "frontend/src/components/about/About.jsx",

        # ui
        "frontend/src/components/ui/CodeWindowTerminal.jsx",
        "frontend/src/components/ui/SectionHeader.jsx",
        "frontend/src/components/ui/Button.jsx",

        # skills
        "frontend/src/components/skills/SkillsGrid.jsx",

        # experience
        "frontend/src/components/experience/ExperienceTimeline.jsx",

        # projects
        "frontend/src/components/projects/ProjectsGrid.jsx",
        "frontend/src/components/projects/ProjectCard.jsx",

        # contact
        "frontend/src/components/contact/Contact.jsx",

        # animations
        "frontend/src/animations/Reveal.jsx",
        "frontend/src/animations/transitions.js",

        # root-level files
        "frontend/tailwind.config.cjs",
        "frontend/postcss.config.cjs",
        "frontend/vite.config.js",
        "frontend/package.json",
        "frontend/.gitignore",
        "frontend/README.md",
    ]

    # ===========================
    # Create Directories
    # ===========================
    for directory in directories:
        dir_path = os.path.join(root_path, directory)
        os.makedirs(dir_path, exist_ok=True)
        print(f"Created directory: {dir_path}")

    # ===========================
    # Create Files
    # ===========================
    for file in files:
        file_path = os.path.join(root_path, file)

        # Ensure parent directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        create_file(file_path)
        print(f"Created file: {file_path}")

    print("\nProject structure created successfully!")


if __name__ == "__main__":
    # Example:
    root_directory = "C:\\Aditya Stuff\\Career\\Portfolio\\frontend"

    if root_directory.strip() == "":
        print("Please provide a valid root directory.")
    else:
        create_structure(root_directory)
