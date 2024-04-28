from setuptools import setup, find_packages
import pathlib

# Read the contents of README file
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='notolog',
    version='0.9.0b0',
    description='Markdown Editor',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/notolog/notolog-editor',
    author='Vadim Bakhrenkov',
    entry_points={
        'console_scripts': [
            'notolog=main:main',
        ],
    },
    classifiers=[
        # More info https://pypi.org/classifiers/
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3 :: Only',
    ],
    packages=find_packages(),  # Find all packages in the directory
    python_requires='>=3.9, <4',
    install_requires=[line.strip() for line in open("requirements.txt", "r")],
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/notolog/notolog-editor/issues',
        'Source': 'https://github.com/notolog/notolog-editor/',
    },
)