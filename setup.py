from setuptools import (
    setup,
    find_packages,
)

version = '1.0.3'

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='PyFiveSim',
    version=version,

    author='Belyashik2K',
    author_email='work@belyashik2k.ru',

    license='MIT license',

    long_description=long_description,
    long_description_content_type='text/markdown',

    description='Sync/async Python wrapper for 5sim API',
    url='https://github.com/Belyashik2K/PyFiveSim',

    packages=find_packages(),

    install_requires=['certifi', 'aiohttp', 'pydantic[email]', 'httpx'],
    zip_safe=False
)
