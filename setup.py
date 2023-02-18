from setuptools import setup, find_packages

setup(
    name='your_package_name',
    version='1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
        'argparse',
        'math',
        'os',
        'argparse'
        
    ],
    entry_points={
        'console_scripts': [
            'map.py=map.py.map:main'
        ]
    }
)