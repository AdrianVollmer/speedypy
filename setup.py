import setuptools
from speedypy._meta import __version__, __doc__

setuptools.setup(
    name='speedypy',
    version=__version__,
    author='Adrian Vollmer',
    url='https://github.com/AdrianVollmer/speedypy',
    description=__doc__,
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'speedypy=speedypy.__main__:main'
        ],
    },
    install_requires=[
        'speedtest-cli',
        'numpy',
        'matplotlib',
        'pyxdg',
    ],
    python_requires='>=3.5',
    tests_require=[
        'pytest',
        'tox',
        'flake8',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
