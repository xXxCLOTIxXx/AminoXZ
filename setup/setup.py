from setuptools import setup, find_packages

with open("README.md", "r") as file:
    long_description = file.read()

link = 'https://github.com/xXxCLOTIxXx/AminoXZ/archive/refs/heads/main.zip'
ver = '1.1.9'

setup(
    name = "AminoXZ",
    version = ver,
    url = "https://github.com/xXxCLOTIxXx/AminoXZ",
    download_url = link,
    license = "MIT",
    author = "Xsarz",
    author_email = "xsarzy@gmail.com",
    description = "Library for creating amino bots and scripts.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    keywords = [
        "aminoapps",
        "aminoxz",
        "amino",
        "amino-bot",
        "narvii",
        "api",
        "python",
        "python3",
        "python3.x",
        "xsarz",
        "official"
    ],
    install_requires = [
        "colored",
        "requests",
        "websocket-client==1.3.1",   
        "websockets",
        "json_minify"

    ],
    packages = find_packages()
)
