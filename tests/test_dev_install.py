from pathlib import Path
import sys

from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
import pytest
import tomli

from dev_install import dependency_requirements, install_dependencies, parse_version


@pytest.mark.parametrize('source,expected', [
    ('^7.4.1', '>=7.4.1,<8.0.0'),
    ('^0.7.0', '>=0.7.0,<0.8.0'),
    ('^0.0.3', '>=0.0.3,<0.0.4'),
    ('>=4.6.2,<4.7', '>=4.6.2,<4.7'),
])
def test_caret_constraints_preserve_compatible_release(source, expected):
    assert parse_version(source) == expected


@pytest.mark.parametrize('python_version', ['3.11', '3.12', '3.13', '3.14'])
def test_development_installer_selects_required_tools(mocker, monkeypatch, python_version):
    monkeypatch.chdir(Path(__file__).resolve().parents[1])
    run = mocker.patch('dev_install.subprocess.run')
    install_dependencies('dev')
    command = run.call_args.args[0]
    assert command[:4] == [sys.executable, '-m', 'pip', 'install']
    assert run.call_args.kwargs == {'check': True}
    requirements = [Requirement(value) for value in command[4:]]
    for name, version in [('pre-commit', '4.7.0'), ('virtualenv', '21.15.6'), ('filelock', '4.2.10')]:
        selected = [req for req in requirements if req.name == name
                    and (req.marker is None or req.marker.evaluate({'python_version': python_version}))]
        assert len(selected) == 1
        assert version in selected[0].specifier


@pytest.mark.parametrize('python_version,numpy_version,markdown_version,genai_version', [
    ('3.11', '2.4.6', '3.11.3', '0.19.0'),
    ('3.12', '2.5.4', '3.11.3', '0.19.0'),
    ('3.13', '2.5.4', '3.11.3', '0.19.0'),
    ('3.14', '2.5.4', '3.11.3', '0.19.0'),
])
def test_runtime_markers_select_one_compatible_branch(python_version, numpy_version, markdown_version, genai_version):
    with (Path(__file__).resolve().parents[1] / 'pyproject.toml').open('rb') as stream:
        dependencies = tomli.load(stream)['tool']['poetry']['dependencies']
    for name, version in [('numpy', numpy_version), ('Markdown', markdown_version), ('onnxruntime-genai', genai_version)]:
        requirements = [Requirement(value) for value in dependency_requirements({name: dependencies[name]})]
        selected = [req for req in requirements
                    if req.marker is None or req.marker.evaluate({'python_version': python_version})]
        assert len(selected) == 1
        assert version in selected[0].specifier


def test_supported_python_versions_match_classifiers():
    with (Path(__file__).resolve().parents[1] / 'pyproject.toml').open('rb') as stream:
        package = tomli.load(stream)['tool']['poetry']
    supported = SpecifierSet(package['dependencies']['python'])
    for minor in range(10, 16):
        version = f'3.{minor}'
        assert (version in supported) == (11 <= minor <= 14)
        classifier = f'Programming Language :: Python :: {version}'
        assert (classifier in package['classifiers']) == (version in supported)
