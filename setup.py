from setuptools import setup, find_packages

INFO = {'name': 'mecode',
        'version': '1.0',
        'description': 'Simple GCode generator',
        'author': 'Daniel Simone',
        'author_email': 'dsimone@princeton.edu',
        }

setup(
    name=INFO['name'],
    version=INFO['version'],
    description=INFO['description'],
    author=INFO['author'],
    author_email=INFO['author_email'],
    packages=find_packages(),
    url='https://github.com/DanielSimone/mecode',
    download_url='https://github.com/DanielSimone/mecode/archive/refs/heads/master.zip',
    keywords=['gcode', '3dprinting', 'cnc', 'reprap', 'additive'],
    zip_safe=False,
    package_data = {
        '': ['*.txt', '*.md'],
    },
    install_requires=[
        'numpy',
        'matplotlib',
        'solidpython',
        'vpython',
    ],
)
