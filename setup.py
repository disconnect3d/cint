import os
from setuptools import setup, find_packages

BASE_DIR = os.path.abspath(path.dirname(__file__))

with open(os.path.join(BASE_DIR, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='cint',
    description='cint - make ctypes great again',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='cint ctypes int integer integers',
    url='https://github.com/disconnect3d/cint',
    version='1.0.0',
    author='disconnect3d',
    author_email='dominik.b.czarnota+cint@gmail.com',
    packages=find_packages(),
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,<4',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
