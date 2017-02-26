from distutils.core import setup
from setuptools import find_packages

setup(
    name='Arbitrage',
    version='1',
    url='https://github.com/tinoater/LollingAllOverTheWorld.git',
    license='',
    author='bobby',
    author_email='',
    description='',
    packages=find_packages(exclude=('Tests', 'Files', 'Results', 'SummaryResults'))
)
