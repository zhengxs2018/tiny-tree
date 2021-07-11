#!/usr/bin/env python3

from os import path
from codecs import open
from setuptools import setup


cwd = path.abspath(path.dirname(__file__))

with open(path.join(cwd, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='tiny-tree',
    version='0.1.0',
    keywords=[
        'tree',
        'array2tree',
        'tree2array',
        'array to tree',
        'data-structures'
    ],
    description='一个循环解决行转树的问题，快速，轻量，无依赖。',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/zhengxs2018/tiny-tree',
    project_urls={
        'Source': 'https://github.com/zhengxs2018/tiny-tree/',
        'Bug Tracker': 'https://github.com/zhengxs2018/tiny-tree/issues',
    },
    packages=['tiny_tree'],
    classifiers=[
        'Topic :: Software Development',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires=">=3.6",
    author='zhengxs',
    author_email='zhengxs2018@foxmail.com',
    maintainer='zhengxs',
    maintainer_email='zhengxs2018@foxmail.com',
    license='MIT'
)
