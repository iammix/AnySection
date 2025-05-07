from setuptools import setup, find_packages

setup(
    name='anysection',
    version='0.1.0',
    author='Konstantinos Mixios',
    author_email='k.mixios@gmail.com',
    description='A Python library for reinforced concrete and steel section analysis',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/iammix/anysection',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
