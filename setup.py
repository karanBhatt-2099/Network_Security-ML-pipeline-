from setuptools import setup, find_packages
from typing import List

def get_requirements()-> List[str]:
    requirement_lst:List[str]=[]
    try:
        with open('requirements.txt','r') as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                if requirement and requirement!= '-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found.")
    return requirement_lst

print(get_requirements())

setup(
    name='Network-Security-MLops',
    version='0.0.1',
    author='Karan',
    author_email='karanbhatt08@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements(),
)