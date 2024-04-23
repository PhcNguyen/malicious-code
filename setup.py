from setuptools import setup


def __version__() -> str:
     return open('scripts/.version', 'r').read()

setup(
    name="Pngz",
    version=__version__(),
    author='PhcNguyen',
    author_email='nguyen098xx@gmail.com',
)