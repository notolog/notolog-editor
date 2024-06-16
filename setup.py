from setuptools import setup, find_packages
import pathlib

# Read the contents of README file
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='notolog',
    version='0.9.5b1',
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
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
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
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: Dutch',
        'Natural Language :: English',
        'Natural Language :: Finnish',
        'Natural Language :: French',
        'Natural Language :: Georgian',
        'Natural Language :: German',
        'Natural Language :: Greek',
        'Natural Language :: Hindi',
        'Natural Language :: Italian',
        'Natural Language :: Japanese',
        'Natural Language :: Korean',
        'Natural Language :: Latin',
        'Natural Language :: Portuguese',
        'Natural Language :: Russian',
        'Natural Language :: Spanish',
        'Natural Language :: Swedish',
        'Natural Language :: Turkish',
    ],
    packages=find_packages(),  # Find all packages in the directory
    include_package_data=True,  # Include data files specified in MANIFEST.in
    python_requires='>=3.9, <3.13',
    install_requires=[line.strip() for line in open("requirements.txt", "r")],
    setup_requires=[
        'build',
        'setuptools',
        'wheel',
    ],
    extras_require={
        'dev': [line.strip() for line in open("dev_requirements.txt", "r")],  # Development dependencies
        'test': [line.strip() for line in open("test_requirements.txt", "r")]  # Test dependencies
    },
    project_urls={
        'Bug Reports': 'https://github.com/notolog/notolog-editor/issues',
        'Source': 'https://github.com/notolog/notolog-editor/',
    },
    keywords='notolog, python, markdown, editor, ai, llm, text, notes',
)
