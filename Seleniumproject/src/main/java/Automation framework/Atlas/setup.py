from setuptools import setup, find_packages

setup(
    name="ATLAS",
    version="1.0.0",
    author="Muthulakshmanan Nagarajan",
    author_email="muthulakshmanan.nagarajan@teradyne.com",
    description="A Python framework for test automation",
    packages=find_packages(),  # Automatically finds all packages
    install_requires=[
        # List dependencies here
        "pytest",
        "allure-pytest",
        "allure-behave",
        "behave",
        "paramiko"

        # Add other dependencies your project needs
    ],
    python_requires=">=3.7",
)
