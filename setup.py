from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='watchcat',
    version='1.0.2',
    author='developnya',
    author_email='developnyaa@gmail.com',
    description='Watchcat - is hot reloader for your project!',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/dop3file/watchcat',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3.11',
    ],
    keywords='watchcat watchdogs reloader',
    python_requires='>=3.11'
)
