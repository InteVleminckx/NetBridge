from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="netbridge",
    version="0.1.0",
    author="Inte Vleminckx",
    author_email="inte.vleminckx14@hotmail.com",
    description="An easy way to interact with your existing code using another script.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=["netbridge", "netbridge/client", "netbridge/server"],
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

