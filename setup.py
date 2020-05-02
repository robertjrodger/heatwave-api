from setuptools import setup, find_packages

test_dependencies = ["pytest", "pytest-cov"]

lint_dependencies = ["flake8"]

setup(
    name="heatwave-api",
    description="Dutch Heatwave Records Service",
    version="1.0.0",
    url="https://github.com/robertjrodger/heatwave-api",
    maintainer="Robert Rodger",
    maintainer_email="woodenrabbit@gmail.com",
    packages=find_packages(include=["src"]),
    package_dir={"": "src"},
    install_requires=[],
    extras_requires={
        "test": test_dependencies,
        "lint": lint_dependencies,
        "dev": test_dependencies + lint_dependencies,
    },
)
