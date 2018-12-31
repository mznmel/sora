import setuptools

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='sora',
    version='0.1',
    description='A simple and unified library to display images in Jupyter notebooks',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/mznmel/sora',
    author='Mazen A. Melibari',
    author_email='mazen@mazen.ws',
    license='MIT',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
