from setuptools import setup, find_packages

setup(
    name='cint',
    description='cint - make ctypes great again',
    url='https://github.com/disconnect3d/cint',
    version='1.0.0',
    author='disconnect3d',
    author_email='dominik.b.czarnota+cint@gmail.com',
    packages=find_packages(),
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ]
)
