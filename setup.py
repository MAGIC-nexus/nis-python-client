from setuptools import setup

setup(
    name='nis',
    version='0.1',
    packages=['nis'],
    install_requires=['typing', 'requests', 'pandas'],
    python_requires='>=3.6',
    url='',
    license='MIT',
    author='rnebot',
    author_email='rnebot@itccanarias.org',
    description='Python client to NIS backend'
)

