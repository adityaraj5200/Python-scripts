import os

def create_file(path):
    """Helper function to create an empty file."""
    with open(path, "w") as f:
        pass

def create_structure(root_path):
    """
    Creates the full project structure inside the existing backend folder.
    root_path must be the path to 'backend/' directory.
    Example: root_path = r"C:/Users/Aditya/Desktop/backend"
    """

    # =======================
    # Directory Structure Map
    # =======================
    directories = [
        "src/main/java/com/aditya/portfolio/controller",
        "src/main/java/com/aditya/portfolio/service/impl",
        "src/main/java/com/aditya/portfolio/model",
        "src/main/java/com/aditya/portfolio/util",
        "src/main/java/com/aditya/portfolio/config",
        "src/main/resources/content",
        "src/main/resources/static",  # optional
    ]

    files = [
        "src/main/java/com/aditya/portfolio/PortfolioBackendApplication.java",

        # Controllers
        "src/main/java/com/aditya/portfolio/controller/AboutController.java",
        "src/main/java/com/aditya/portfolio/controller/SkillsController.java",
        "src/main/java/com/aditya/portfolio/controller/ExperienceController.java",
        "src/main/java/com/aditya/portfolio/controller/ProjectsController.java",
        "src/main/java/com/aditya/portfolio/controller/EducationController.java",
        "src/main/java/com/aditya/portfolio/controller/ContactController.java",

        # Services
        "src/main/java/com/aditya/portfolio/service/ContentService.java",
        "src/main/java/com/aditya/portfolio/service/impl/ContentServiceImpl.java",

        # Models
        "src/main/java/com/aditya/portfolio/model/About.java",
        "src/main/java/com/aditya/portfolio/model/Skills.java",
        "src/main/java/com/aditya/portfolio/model/Experience.java",
        "src/main/java/com/aditya/portfolio/model/Project.java",
        "src/main/java/com/aditya/portfolio/model/ProjectsWrapper.java",
        "src/main/java/com/aditya/portfolio/model/Education.java",
        "src/main/java/com/aditya/portfolio/model/Contact.java",

        # Util
        "src/main/java/com/aditya/portfolio/util/JsonLoader.java",
        "src/main/java/com/aditya/portfolio/util/CustomException.java",

        # Config
        "src/main/java/com/aditya/portfolio/config/WebConfig.java",
        "src/main/java/com/aditya/portfolio/config/CORSConfig.java",
        "src/main/java/com/aditya/portfolio/config/SwaggerConfig.java",

        # Resource JSON files
        "src/main/resources/content/about.json",
        "src/main/resources/content/skills.json",
        "src/main/resources/content/experience.json",
        "src/main/resources/content/projects.json",
        "src/main/resources/content/education.json",
        "src/main/resources/content/contact.json",

        # Static file
        "src/main/resources/static/profile.jpg",   # optional placeholder

        # Resource files
        "src/main/resources/application.properties",
        "src/main/resources/banner.txt",           # optional

        # Root-level files
        ".gitignore",
        "pom.xml",
        "README.md"
    ]

    # =======================
    # Create Directories
    # =======================
    for directory in directories:
        dir_path = os.path.join(root_path, directory)
        os.makedirs(dir_path, exist_ok=True)
        print(f"Created directory: {dir_path}")

    # =======================
    # Create Files
    # =======================
    for file in files:
        file_path = os.path.join(root_path, file)

        # Ensure parent directory exists (safety)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        create_file(file_path)
        print(f"Created file: {file_path}")

    print("\nProject structure created successfully!")


if __name__ == "__main__":
    # =======================
    #   PLACEHOLDER INPUT
    # =======================
    root_directory = "C:\\Aditya Stuff\\Career\\My portfolio\\backend"  # <-- PUT YOUR backend/ FOLDER PATH HERE

    if root_directory.strip() == "":
        print("Please provide the path to the backend directory in the script.")
    else:
        create_structure(root_directory)
