"""distutils setup file"""

import setuptools

SUPPLEMENTARY = {
    "test": [
        # "codecov>=2.0.22,<2.1",
        "coverage>=5.1,<5.2",
        "flake8==3.7.9",
        "flake8-commas>=2.0.0,<2.1",
        "flake8-isort>=3.0.0,<3.1",
        "flake8-quotes>=2.1.1,<2.2",
        "isort>=4.3.21,<4.4",
        "pylint>=2.4.4,<2.5",
        "pytest>=5.4,<5.5",
        "pytest-cov>=2.8.1,<2.9",
        "pytest-flake8>=1.0.4,<1.1",
        "pytest-pylint>=0.15.1,<0.16",
    ]}

setuptools.setup(
    name="robobisect",
    version="0.0.1a1",
    description="Bisect the WebKit Git repository to find regression windows",
    classifiers=[
        # complete classifier list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Testing",
        "Topic :: Utilities",
    ],
    keywords=[
        "bisection", "git",
    ],
    url="https://github.com/nth10sd/robobisect",
    entry_points={
        "console_scripts": ["robobisect = robobisect.start:main"],
    },
    package_data={"robobisect": [
        "util/*",
    ]},
    packages=setuptools.find_packages(include=["robobisect"]),
    # install_requires=[
    # ],
    extras_require=SUPPLEMENTARY,
    python_requires=">=3.6",
    zip_safe=False,
)
