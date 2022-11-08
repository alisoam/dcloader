from distutils.core import setup

setup(
    name="dcloader",
    packages=["dcloader"],
    package_dir={"dcloader": "dcloader"},
    version="0.1.3",
    description="",
    author="Ali Sorour Amini",
    author_email="ali.sorouramini@gmail.com",
    url="https://github.com/alisoam/dcloader",
    install_requires=["PyYAML==6.0.*"],
)
