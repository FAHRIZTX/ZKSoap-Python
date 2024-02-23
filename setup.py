import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
   name='zksoap',
   version='0.0.5',
   author='Muhammad Fahri',
   author_email='admin+tech@fahriztx.dev',
   long_description = long_description,
   long_description_content_type = "text/markdown",
   package_dir = {"": "src"},
   packages = setuptools.find_packages(where="src"),
   python_requires = ">=3.6",
   license='MIT',
   url='https://github.com/FAHRIZTX/ZKSoap-Python'
)
