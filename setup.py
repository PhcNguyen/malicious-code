from setuptools import find_packages, setup


def __version__() -> str:
     return open('scripts/.version', 'r').read()

setup(
    name="Pngz",
    version=__version__(),
    author='PhcNguyen',
    author_email='nguyen098xx@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements("docs/requirements.txt"),
)