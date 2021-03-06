# coding=utf-8

import os
from setuptools import setup, find_packages


def get_version():
    basedir = os.path.dirname(__file__)
    try:
        with open(os.path.join(basedir, 'tddude/version.py')) as f:
            loc = {}
            exec(f.read(), loc)
            return loc['VERSION']
    except:
        raise RuntimeError('No version info found.')

setup(
    name='tddude',
    version=get_version(),
    url='https://github.com/sancau/tddude/',
    license='MIT',
    author='Alexander Tatchin',
    author_email='alexander.tatchin@gmail.com',
    description='Development tool for TDD workflow automation.',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'fire>=0.1.0',
        'pytest>=3.0.7',
        'watchdog>=0.8.3'
    ],
    entry_points={
        'console_scripts': [
            'tddude = tddude.tddude:main'
        ],
    },
    classifiers=[
        #  As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)