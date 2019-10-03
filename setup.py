import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="parrec-reader-py",
    version="0.0.1",
    author="Martin Bührer",
    author_email="info@gyrotools.com",
    description="A Philips par/rec reader for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gyrotools/parrec-reader-py",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy'
    ],
    python_requires='>=3.6.0',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
