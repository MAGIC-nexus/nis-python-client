# ONE TIME  -----------------------------------------------------------------------------
#
# pip install --upgrade setuptools wheel twine
#
# Create account:
# PyPI test: https://test.pypi.org/account/register/
# or PyPI  : https://pypi.org/account/register/
#
# EACH TIME -----------------------------------------------------------------------------
#
# Modify version code in "setup.py" (this file)
#
# Build:
# python3 setup.py sdist bdist_wheel
#
# Upload:
# PyPI test: twine upload --skip-existing --repository-url https://test.pypi.org/legacy/ dist/*
# or PyPI  : twine upload --skip-existing dist/*
#
# INSTALL   ------------------------------------------------------------------------------
#
# PyPI test: pip install --index-url https://test.pypi.org/simple/ --upgrade nexinfosys-client
# PyPI     : pip install --upgrade nexinfosys-client
# No PyPI  : pip install -e <local path where "setup.py" (this file) is located>
#


from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    version='0.21',
    name='nexinfosys-client',
    packages=['nexinfosys'],
    install_requires=['requests', 'pandas', 'webdavclient==1.0.8'],
    python_requires='>=3.6',
    url='https://github.com/MAGIC-nexus/nis-python-client',
    license='BSD3',
    author='Rafael Nebot - ITC, SA - DCCT',
    author_email='rnebot@itccanarias.org',
    long_description=long_description,
    long_description_content_type='text/markdown',
    description='Client to NIS backend'
)

