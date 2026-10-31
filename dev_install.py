"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Part of the development and testing environment.
- Functionality: Allows running development-related checks and setup.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

import sys
import argparse
import subprocess
import tomli


def parse_version(version):
    if version.startswith('^'):
        parts = [int(part) for part in version[1:].split('.')]
        index = next((i for i, part in enumerate(parts) if part), len(parts) - 1)
        upper = parts[:index] + [parts[index] + 1] + [0] * (len(parts) - index - 1)
        return f">={version[1:]},<{'.'.join(map(str, upper))}"
    return version


def dependency_requirements(dependencies):
    """Convert the project's version constraints and markers into pip requirements."""
    for name, declarations in dependencies.items():
        if not isinstance(declarations, list):
            declarations = [declarations]
        for declaration in declarations:
            if isinstance(declaration, str):
                yield f'{name}{parse_version(declaration)}'
            else:
                requirement = f"{name}{parse_version(declaration['version'])}"
                if declaration.get('markers'):
                    requirement += f"; {declaration['markers']}"
                yield requirement


def install_dependencies(group):
    with open('pyproject.toml', 'rb') as f:
        data = tomli.load(f)

    dependencies = data.get('tool', {}).get('poetry', {}).get('group', {}).get(group, {}).get('dependencies', {})

    packages = list(dependency_requirements(dependencies))
    if packages:
        subprocess.run([sys.executable, "-m", "pip", "install"] + packages, check=True)


def show_help():
    """
    Install Notolog's development and testing packages to ensure the software's quality and functionality.

    Usage:
        python dev_install.py [dev|test|all|help]

    Arguments:
        dev  - Install development tools necessary for coding and quality checks.
        test - Install testing tools required for running test suites.
        all  - Install both development and testing tools.
        help - Displays a detailed help message.

    Examples:
        Install development tools:
            python dev_install.py dev

        Install testing tools:
            python dev_install.py test

        Install all tools:
            python dev_install.py all

        Display this help message:
            python dev_install.py help

    This script helps manage dependencies in a targeted way, allowing for a streamlined setup process.
    """
    return show_help.__doc__


class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        # sys.stderr.write(f'Error: {message}\n')
        self.print_help()
        sys.exit(2)


def main():
    # Setup command-line argument parsing.
    # Default: argparse.ArgumentParser()
    parser = CustomArgumentParser(description="Install development, testing, or all packages.")
    parser.add_argument('package', nargs='?', default='all', choices=['all', 'dev', 'test', 'help'],
                        help="Specify the package type to install: 'all', 'dev', 'test', or 'help'.")

    args = parser.parse_args()

    if args.package == 'help':
        print(show_help())
        sys.exit(0)

    if args.package == 'all':
        # Ask for confirmation before installing all packages
        response = input("This will install all dev and test packages. Proceed? (y/n): ")
        if response.lower() == 'y':
            install_dependencies('dev')
            install_dependencies('test')
        else:
            print("Installation cancelled.")
    elif args.package in ['dev', 'test']:
        install_dependencies(args.package)
    else:
        # This will only be reached if argparse allows an unexpected argument,
        # which should be prevented by argparse setup
        parser.print_help()


if __name__ == "__main__":
    main()
