from setuptools import setup, find_packages
import pathlib

# Read the contents of README file
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='notolog',
    version='0.9.1b5',
    description='Notolog - Python Markdown Editor',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/notolog/notolog-editor',
    author='Vadim Bakhrenkov',
    license='MIT',
    # py_modules=['main'],  # This refers to the standalone 'main.py' at the top-level directory
    entry_points={
        'console_scripts': [
            # 'notolog=main:main',  # main.py at the top-level directory
            'notolog=notolog.main:main',  # main.py within the main package
        ],
    },
    classifiers=[
        # More info https://pypi.org/classifiers/
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Text Editors',
        'Topic :: Text Editors :: Documentation',
        'Topic :: Text Editors :: Emacs',
        'Topic :: Text Editors :: Integrated Development Environments (IDE)',
        'Topic :: Text Editors :: Text Processing',
        'Topic :: Text Editors :: Word Processors',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: General',
        'Topic :: Text Processing :: Markup :: Markdown',
    ],
    packages=find_packages(),  # Find all packages in the directory
    include_package_data=True,  # Include data files specified in MANIFEST.in
    python_requires='>=3.9, <4',
    install_requires=[line.strip() for line in open("requirements.txt", "r")],
    project_urls={
        'Bug Reports': 'https://github.com/notolog/notolog-editor/issues',
        'Source': 'https://github.com/notolog/notolog-editor/',
    },
    keywords='notolog, python, markdown, editor, ai, text, notes',
)
