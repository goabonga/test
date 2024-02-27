from setuptools import find_packages, setup

import playground

setup(
    name="playground",
    version=playground.__version__,
    author="Chris",
    author_email="goabonga@pm.me",
    description="Minimal python project.",
    # long_description=open('README.md').read(),
    # long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        "click==8.1.7",
    ],
    extras_require={
        "dev": [
            "pytest==7.1.3",
            "pytest-cov==4.1.0",
            "mock==5.1.0",
            "black==23.3.0",
            "isort==5.12.0",
            "flake8==6.0.0",
            "autoflake==2.3.0",
        ]
    },
    entry_points={"console_scripts": [f"playground=playground.hello:hello"]},
)
