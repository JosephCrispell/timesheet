from setuptools import setup

from timesheet import __version__

setup(
    name="my_pip_package",
    version=__version__,
    url="https://github.com/JosephCrispell/timesheet",
    author="JosephCrispell",
    author_email="test@mail.com",
    py_modules=["timesheet"],
)
