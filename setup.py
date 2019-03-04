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

setup(
    name='nexinfosys-client',
    version='0.16',
    packages=['nexinfosys'],
    install_requires=['requests', 'pandas', 'webdavclient'],
    python_requires='>=3.6',
    url='',
    license='MIT',
    author='rnebot',
    author_email='rnebot@itccanarias.org',
    description='Python client to NIS backend'
)

