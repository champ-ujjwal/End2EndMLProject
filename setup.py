from setuptools import setup, find_packages
from typing import List  # import all req.txt contents in a list


def get_requirements(file_path: str) -> List[str]:
    """
    This function will return the list of requirements
    """
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]
        if '-e .' in requirements:
            requirements.remove('-e .')
    return requirements





setup(
    name="ML PROJECT",
    version="0.0.1",
    author="Ujjwal Singh",
    author_email="cs24resch11014@iith.ac.in",
    description="A small ML project",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)