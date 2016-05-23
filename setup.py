try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'A Python program to show/analyse Taiwan stock data that got from Yahoo! Finance.',
    'author': 'kueihua chang',
    'url': 'https://github.com/kueihua100/TwanStkEx2',
    'download_url': 'https://github.com/kueihua100/TwanStkEx2',
    'author_email': 'kueihua.chang@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['TwanStkEx2'],
    'scripts': [],
    'name': 'TwanStkEx2'
}

setup(**config)