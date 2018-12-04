import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CostumePy",
    version="0.0.1",
    author="Samuel Martin",
    author_email="sam@codematerial.com",
    description="A distributed messaging system for wearable tech",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/codematerial/CostumePy",
    packages=setuptools.find_packages(),
    install_requires =["zmq"]
)