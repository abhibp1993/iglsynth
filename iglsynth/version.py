
# Versioning scheme is Major.Minor.Micro
# Minor and Major are changed when there are breaking changes or stable versions are released.
_major = 0
_minor = 2
_micro = 3
_build = 0                                                  # Reason: Dockerfiles updated
__version__ = f"{_major}.{_minor}.{_micro}"

# Contributors
__author__ = ["Abhishek N. Kulkarni"]


def get_publish_version():
    return __version__


def get_build_version():
    return f"{_major}.{_minor}.{_micro}.{_build}"


def author():
    return __author__
