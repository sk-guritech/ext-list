from __future__ import annotations

from setuptools import setup

with open('README.md', encoding='utf-8') as readme_md:
    long_description = readme_md.read()

setup(
    name='ext-list',
    version='1.1.1',
    author='Sakaguchi Ryo',
    author_email='sakaguchi@sk-techfirm.com',
    description='This is a utility library that extends Python\'s list operations.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sk-guritech/ext-list',
    project_urls={
        'Bug Tracker': 'https://github.com/sk-guritech/ext-list/issues',
    },
    classifiers=[
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Typing :: Typed',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    keywords=['list', 'comprehension', 'iterable', 'code quality'],
    packages=['ext_list'],
    python_requires='>=3.7',
    install_requires=['typing_extensions'],
)
