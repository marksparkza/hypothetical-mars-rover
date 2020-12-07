from setuptools import setup, find_packages

setup(
    name='Hypothetical Mars Rover',
    packages=find_packages(),
    python_requires='~=3.8',
    install_requires=[],
    extras_require={'test': ['pytest', 'hypothesis']},
)
