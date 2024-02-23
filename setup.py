import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
   name='zksoap',
   version='0.0.6',
   author='Muhammad Fahri',
   author_email='admin@fahriztx.dev',
   long_description = long_description,
   long_description_content_type = "text/markdown",
   package_dir = {"": "src"},
   packages = setuptools.find_packages(where="src"),
   python_requires = ">=3.6",
   license='MIT',
   url='https://fahriztx.dev/',
   project_urls = {
    "Bug Tracker": "https://github.com/FAHRIZTX/ZKSoap-Python/issues",
    "Documentation": "https://github.com/FAHRIZTX/ZKSoap-Python/blob/master/README.md",
    "Source Code": "https://github.com/FAHRIZTX/ZKSoap-Python",
   }
)
