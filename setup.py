from setuptools import setup, find_packages

setup(
    name='soxutils',
    version='0.0.1',
    author='Takano, Takeshi',
    author_email='takano.tak@gmail.com',
    packages=find_packages(),
    install_requires=["sox"],
    entry_points={'console_scripts': 'soxdir=soxutils:soxdir'}
)