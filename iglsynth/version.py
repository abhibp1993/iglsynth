
# Versioning scheme is Major.Minor.Micro
# Minor and Major are changed when there are breaking changes or stable versions are released.
_major = 1
_minor = 0
_micro = 0
_build = 1
__version__ = f"{_major}.{_minor}.{_micro}"

# Contributors
__author__ = ["Abhishek N. Kulkarni"]


def get_publish_version():
    return __version__


def get_build_version():
    return f"{_major}.{_minor}.{_micro}.{_build}"


def author():
    return __author__
