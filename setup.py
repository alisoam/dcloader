from distutils.core import setup

setup(
    name="dcloader",
    packages=["dcloader"],
    package_dir={"dcloader": "dcloader"},
    package_data={"dcloader": ["py.typed"]},
    version="0.6.0",
    description="",
    author="Ali Sorour Amini",
    author_email="ali.sorouramini@gmail.com",
    url="https://github.com/alisoam/dcloader",
    install_requires=["PyYAML==6.0.*"],
)
