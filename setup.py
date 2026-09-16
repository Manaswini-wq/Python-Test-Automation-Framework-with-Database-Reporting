from setuptools import setup, find_packages

setup(
    name="test-automation-framework",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pymongo>=4.6",
        "pyyaml>=6.0",
        "jinja2>=3.1",
    ],
    entry_points={
        "console_scripts": [
            "testrunner=framework.core.test_runner:main",
        ],
    },
)
