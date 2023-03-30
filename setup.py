from __future__ import annotations

from setuptools import setup

with open('README.md', encoding='utf-8') as readme_md:
    long_description = readme_md.read()

setup(
    name='ex-list',
    version='0.1.2',
    author='Sakaguchi Ryo',
    author_email='',
    description='ExList is a Python library that improves code quality by allowing list comprehension operations to be called as methods and handling lists more abstractly than the built-in list. It reduces list comprehensions, improving code readability and searchability. Add, ExList enforces a single type iterable object, leading to a simpler program structure.',  # noqa: E501
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/GuriTech/exlist',
    project_urls={
        'Bug Tracker': 'https://github.com/GuriTech/exlist/issues',
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords=['list', 'comprehension', 'iterable', 'code quality'],
    packages=['.'],
    python_requires='>=3.10',
    install_requires=['typing_extensions'],
)
