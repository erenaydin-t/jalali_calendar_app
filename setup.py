from setuptools import setup, find_packages
import re
import ast

# Get version from __version__ variable without importing the module
_version_re = re.compile(r'__version__\s+=\s+(.*)')
with open('jalali_calendar/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="jalali_calendar",
    version=version,
    description="Jalali (Shamsi) Calendar for ERPNext",
    author="Eren Aydin",
    author_email="****@gmail.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
