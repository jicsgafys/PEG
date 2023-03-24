import os


def project_path():
    # This function gets the absolute path of the project directory
    path = os.path.dirname(os.path.abspath(__file__)).rstrip('utils')

    return path


DISK_ROOT_PATH = project_path().split(":")[0] + ":\\"
PROJECT_ROOT_PATH = project_path()
IMAGES_FOLDER_PATH = os.path.join(project_path(), 'assets\\images\\')
ICONS_FOLDER_PATH = os.path.join(project_path(), 'assets\\icons\\')
DATABASE_FOLDER_PATH = os.path.join(project_path(), 'database\\')
DATABASE_FILE_PATH = os.path.join(project_path(), 'database\\database.db')
