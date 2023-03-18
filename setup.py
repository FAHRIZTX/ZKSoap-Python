from setuptools import find_packages, setup

setup(
   name='zksoap',
   packages={"zksoap": "src/fahriztx"},
   version='0.1.0',
   description='A PHP Library For Manage Data From Fingerprint Machine with SOAP Protocol',
   author='Muhammad Fahri',
   license='MIT',
   install_requires=[],
   setup_requires=['pytest-runner'],
   tests_require=['pytest'],
   test_suite='test',
)