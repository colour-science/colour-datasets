# -*- coding: utf-8 -*-
"""
Invoke - Tasks
==============
"""

import biblib.bib
import fnmatch
import os
import re
import uuid
from invoke import task

import colour_datasets
from colour.utilities import message_box

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2019-2021 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-developers@colour-science.org'
__status__ = 'Production'

__all__ = [
    'APPLICATION_NAME', 'APPLICATION_VERSION', 'PYTHON_PACKAGE_NAME',
    'PYPI_PACKAGE_NAME', 'BIBLIOGRAPHY_NAME', 'clean', 'formatting', 'tests',
    'quality', 'examples', 'preflight', 'docs', 'todo', 'requirements',
    'build', 'virtualise', 'tag', 'release', 'sha256'
]

APPLICATION_NAME = colour_datasets.__application_name__

APPLICATION_VERSION = colour_datasets.__version__

PYTHON_PACKAGE_NAME = colour_datasets.__name__

PYPI_PACKAGE_NAME = 'colour-datasets'

BIBLIOGRAPHY_NAME = 'BIBLIOGRAPHY.bib'


@task
def clean(ctx, docs=True, bytecode=False):
    """
    Cleans the project.

    Parameters
    ----------
    ctx : invoke.context.Context
        Context.
    docs : bool, optional
        Whether to clean the *docs* directory.
    bytecode : bool, optional
        Whether to clean the bytecode files, e.g. *.pyc* files.

    Returns
    -------
    bool
        Task success.
    """
    message_box('Cleaning project...')

    patterns = ['build', '*.egg-info', 'dist']

    if docs:
        patterns.append('docs/_build')
        patterns.append('docs/generated')

    if bytecode:
        patterns.append('**/__pycache__')
        patterns.append('**/*.pyc')

    for pattern in patterns:
        ctx.run("rm -rf {}".format(pattern))


@task
def formatting(ctx, yapf=True, asciify=True, bibtex=True):
    """
    Formats the codebase with *Yapf*, converts unicode characters to ASCII and
    cleanup the "BibTeX" file.

    Parameters
    ----------
    ctx : invoke.context.Context
        Context.
    yapf : bool, optional
        Whether to format the codebase with *Yapf*.
    asciify : bool, optional
        Whether to convert unicode characters to ASCII.
    bibtex : bool, optional
        Whether to cleanup the *BibTeX* file.

    Returns
    -------
    bool
        Task success.
    """

    if yapf:
        message_box('Formatting codebase with "Yapf"...')
        ctx.run('yapf -p -i -r --exclude \'.git\' .')

    if asciify:
        message_box('Converting unicode characters to ASCII...')
        with ctx.cd('utilities'):
            ctx.run('./unicode_to_ascii.py')

    message_box('Cleaning up "BibTeX" file...')
    bibtex_path = BIBLIOGRAPHY_NAME
    with open(bibtex_path) as bibtex_file:
        bibtex = biblib.bib.Parser().parse(bibtex_file.read()).get_entries()

    for entry in sorted(bibtex.values(), key=lambda x: x.key):
        try:
            del entry['file']
        except KeyError:
            pass
        for key, value in entry.items():
            entry[key] = re.sub('(?<!\\\\)\\&', '\\&', value)

    with open(bibtex_path, 'w') as bibtex_file:
        for entry in sorted(bibtex.values(), key=lambda x: x.key):
            bibtex_file.write(entry.to_bib())
            bibtex_file.write('\n')


@task
def tests(ctx, nose=True):
    """
    Runs the unit tests with *Nose* or *Pytest*.

    Parameters
    ----------
    ctx : invoke.context.Context
        Context.
    nose : bool, optional
        Whether to use *Nose* or *Pytest*.

    Returns
    -------
    bool
        Task success.
    """

    if nose:
        message_box('Running "Nosetests"...')
        ctx.run('nosetests --with-doctest --with-coverage '
                '--traverse-namespace --cover-package={0} {0}'.format(
                    PYTHON_PACKAGE_NAME))
    else:
        message_box('Running "Pytest"...')
        ctx.run('py.test --disable-warnings --doctest-modules '
                '--ignore={0}/examples {0}'.format(PYTHON_PACKAGE_NAME))


@task
def quality(ctx, flake8=True, rstlint=True):
    """
    Checks the codebase with *Flake8* and lints various *restructuredText*
    files with *rst-lint*.

    Parameters
    ----------
    ctx : invoke.context.Context
        Context.
    flake8 : bool, optional
        Whether to check the codebase with *Flake8*.
    rstlint : bool, optional
        Whether to lint various *restructuredText* files with *rst-lint*.

    Returns
    -------
    bool
        Task success.
    """

    if flake8:
        message_box('Checking codebase with "Flake8"...')
        ctx.run('flake8 {0} --exclude=examples'.format(PYTHON_PACKAGE_NAME))

    if rstlint:
        message_box('Linting "README.rst" file...')
        ctx.run('rst-lint README.rst')


@task
def examples(ctx):
    """
    Runs the examples.

    Parameters
    ----------
    ctx : invoke.context.Context
        Context.

    Returns
    -------
    bool
        Task success.
    """

    message_box('Running examples...')

    for root, dirnames, filenames in os.walk(
            os.path.join(PYTHON_PACKAGE_NAME, 'examples')):
        for filename in fnmatch.filter(filenames, '*.py'):
            ctx.run('python {0}'.format(os.path.join(root, filename)))


@task(formatting, tests, quality, examples)
def preflight(ctx):
    """
    Performs the preflight tasks, i.e. *formatting*, *tests*, *quality*, and
    *examples*.

    Parameters
    ----------
    ctx : invoke.context.Context
        Context.

    Returns
    -------
    bool
        Task success.
    """

    message_box('Finishing "Preflight"...')


@task
def docs(ctx, html=True, pdf=True):
    """
    Builds the documentation.

    Parameters
    ----------
    ctx : invoke.context.Context
        Context.
    html : bool, optional
        Whether to build the *HTML* documentation.
    pdf : bool, optional
        Whether to build the *PDF* documentation.

    Returns
    -------
    bool
        Task success.
    """

    with ctx.prefix('export COLOUR_SCIENCE__DOCUMENTATION_BUILD=True'):
        with ctx.cd('docs'):
            if html:
                message_box('Building "HTML" documentation...')
                ctx.run('make html')

            if pdf:
                message_box('Building "PDF" documentation...')
                ctx.run('make latexpdf')


@task
def todo(ctx):
    """
    Export the TODO items.

    Parameters
    ----------
    ctx : invoke.context.Context
        Context.

    Returns
    -------
    bool
        Task success.
    """

    message_box('Exporting "TODO" items...')

    with ctx.cd('utilities'):
        ctx.run('./export_todo.py')


@task
def requirements(ctx):
    """
    Exports the *requirements.txt* file.

    Parameters
    ----------
    ctx : invoke.context.Context
        Context.

    Returns
    -------
    bool
        Task success.
    """

    message_box('Exporting "requirements.txt" file...')
    ctx.run('poetry run pip list --format=freeze | '
            'egrep -v "github.com/colour-science" '
            '> requirements.txt')


@task(clean, preflight, docs, todo, requirements)
def build(ctx):
    """
    Builds the project and runs dependency tasks, i.e. *docs*, *todo*, and
    *preflight*.

    Parameters
    ----------
    ctx : invoke.context.Context
        Context.

    Returns
    -------
    bool
        Task success.
    """

    message_box('Building...')
    ctx.run('poetry build')

    with ctx.cd('dist'):
        ctx.run('tar -xvf {0}-{1}.tar.gz'.format(PYPI_PACKAGE_NAME,
                                                 APPLICATION_VERSION))
        ctx.run('cp {0}-{1}/setup.py ../'.format(PYPI_PACKAGE_NAME,
                                                 APPLICATION_VERSION))

        ctx.run('rm -rf {0}-{1}'.format(PYPI_PACKAGE_NAME,
                                        APPLICATION_VERSION))

    with open('setup.py') as setup_file:
        source = setup_file.read()

    setup_kwargs = []

    def sub_callable(match):
        setup_kwargs.append(match)

        return ''

    template = """
setup({0}
)
"""

    source = re.sub('from setuptools import setup',
                    'import codecs\nfrom setuptools import setup', source)
    source = re.sub(
        'setup_kwargs = {(.*)}.*setup\\(\\*\\*setup_kwargs\\)',
        sub_callable,
        source,
        flags=re.DOTALL)[:-2]
    setup_kwargs = setup_kwargs[0].group(1).splitlines()
    for i, line in enumerate(setup_kwargs):
        setup_kwargs[i] = re.sub('^\\s*(\'(\\w+)\':\\s?)', '    \\2=', line)
        if setup_kwargs[i].strip().startswith('long_description'):
            setup_kwargs[i] = ('    long_description='
                               'codecs.open(\'README.rst\', encoding=\'utf8\')'
                               '.read(),')

    source += template.format('\n'.join(setup_kwargs))

    with open('setup.py', 'w') as setup_file:
        setup_file.write(source)

    ctx.run('twine check dist/*')


@task
def virtualise(ctx, tests=True):
    """
    Create a virtual environment for the project build.

    Parameters
    ----------
    ctx : invoke.context.Context
        Context.
    tests : bool, optional
        Whether to run tests on the virtual environment.

    Returns
    -------
    bool
        Task success.
    """

    unique_name = '{0}-{1}'.format(PYPI_PACKAGE_NAME, uuid.uuid1())
    with ctx.cd('dist'):
        ctx.run('tar -xvf {0}-{1}.tar.gz'.format(PYPI_PACKAGE_NAME,
                                                 APPLICATION_VERSION))
        ctx.run('mv {0}-{1} {2}'.format(PYPI_PACKAGE_NAME, APPLICATION_VERSION,
                                        unique_name))
        with ctx.cd(unique_name):
            ctx.run('poetry env use 3')
            ctx.run('poetry install')
            ctx.run('source $(poetry env info -p)/bin/activate')
            if tests:
                ctx.run('poetry run nosetests')


@task
def tag(ctx):
    """
    Tags the repository according to defined version using *git-flow*.

    Parameters
    ----------
    ctx : invoke.context.Context
        Context.

    Returns
    -------
    bool
        Task success.
    """

    message_box('Tagging...')
    result = ctx.run('git rev-parse --abbrev-ref HEAD', hide='both')

    assert result.stdout.strip() == 'develop', (
        'Are you still on a feature or master branch?')

    with open(os.path.join(PYTHON_PACKAGE_NAME, '__init__.py')) as file_handle:
        file_content = file_handle.read()
        major_version = re.search("__major_version__\\s+=\\s+'(.*)'",
                                  file_content).group(1)
        minor_version = re.search("__minor_version__\\s+=\\s+'(.*)'",
                                  file_content).group(1)
        change_version = re.search("__change_version__\\s+=\\s+'(.*)'",
                                   file_content).group(1)

        version = '.'.join((major_version, minor_version, change_version))

        result = ctx.run('git ls-remote --tags upstream', hide='both')
        remote_tags = result.stdout.strip().split('\n')
        tags = set()
        for remote_tag in remote_tags:
            tags.add(
                remote_tag.split('refs/tags/')[1].replace('refs/tags/', '^{}'))
        tags = sorted(list(tags))
        assert 'v{0}'.format(version) not in tags, (
            'A "{0}" "v{1}" tag already exists in remote repository!'.format(
                PYTHON_PACKAGE_NAME, version))

        ctx.run('git flow release start v{0}'.format(version))
        ctx.run('git flow release finish v{0}'.format(version))


@task(build)
def release(ctx):
    """
    Releases the project to *Pypi* with *Twine*.

    Parameters
    ----------
    ctx : invoke.context.Context
        Context.

    Returns
    -------
    bool
        Task success.
    """

    message_box('Releasing...')
    with ctx.cd('dist'):
        ctx.run('twine upload *.tar.gz')
        ctx.run('twine upload *.whl')


@task
def sha256(ctx):
    """
    Computes the project *Pypi* package *sha256* with *OpenSSL*.

    Parameters
    ----------
    ctx : invoke.context.Context
        Context.

    Returns
    -------
    bool
        Task success.
    """

    message_box('Computing "sha256"...')
    with ctx.cd('dist'):
        ctx.run('openssl sha256 {0}-*.tar.gz'.format(PYPI_PACKAGE_NAME))
