import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ppm",
    version="0.0.1",
    author="Adam Weeden",
    author_email="adamweeden@gmail.com",
    description="a package manager for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheCleric/ppm",
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: LGPL License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
    keywords='packages packaging',
    packages=setuptools.find_packages(
        exclude=[
            "tests",
            "tests.*",
        ],
    ),
    install_requires=[],
    extras_require={
        'dev': [
            'autopep8>=1.5.4',
            'setuptools>=50.3.0',
        ],
        'test': [
            'pylint>=2.6.0',
            'pytest>=6.0.2',
            'mypy>=0.782',
            'pytest-cov>=2.10.1',
        ],
    },
    include_package_data=False,
    # package_data={
    #    'sample': ['package_data.dat'],
    # },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    #data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    # entry_points={
    #    'console_scripts': [
    #        'sample=sample:main',
    #    ],
    # },
)
