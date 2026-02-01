#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.14"
# dependencies = ["colorlog>=6.10.1", "pydpkg>=1.9.5"]
# ///

import re
from argparse import ArgumentParser
from collections.abc import Iterator
from dataclasses import dataclass
from logging import Logger
from pathlib import Path
from typing import Literal

from pydpkg import Dpkg


def setup_logger() -> None:
    import logging

    from colorlog import ColoredFormatter

    handler = logging.StreamHandler()
    handler.setFormatter(ColoredFormatter())
    logging.basicConfig(handlers=[handler])


def logger(name: str) -> Logger:
    # logging not imported at module level to avoid mixing names
    import logging

    root = logging.getLogger(__name__)
    return root.getChild(name)


def set_verbosity(level: int | object) -> None:
    import logging

    # set log level globally
    root = logging.getLogger()

    match level:
        case 0:
            root.setLevel(logging.WARNING)
        case 1:
            root.setLevel(logging.INFO)
        case 2:
            root.setLevel(logging.DEBUG)
        case int(_):
            log = logger('set_verbosity')
            log.warning('maximum verbosity exceeded (%d > 2), try -vv only', level)

            root.setLevel(logging.DEBUG)
        case _:
            log = logger('set_verbosity')
            log.error('invalid verbosity: %s', level)
            raise ValueError(level)


setup_logger()

CURRENT_DIRECTORY = Path('.').resolve(strict=True)


def resolve(path: str | Path) -> Path:
    absolute = Path(path).resolve(strict=True)
    try:
        relative = absolute.relative_to(CURRENT_DIRECTORY)
    except ValueError:
        relative = absolute

    log = logger('resolve')
    log.debug('path=%r to %r (%r)', path, relative, absolute)
    return relative


def walk_dir(folder: Path, *, suffix: str) -> Iterator[Path]:
    log = logger('walk_dir')
    log.debug('listing %s in %r', suffix, folder)

    for root, _, files in folder.walk():
        log.debug('in %r: root=%r, files=%r', folder, root, files)
        for file in files:
            target = root.joinpath(file)
            if target.suffix != suffix:
                log.debug('not a %s file, ignored: %r', suffix, target)
                continue

            log.debug('selected: %r', target)
            yield target


def extract_tar(archive: Path, *, suffix: str) -> Iterator[Path]:
    import tarfile
    from tempfile import TemporaryDirectory

    log = logger('extract_tar')
    log.debug('listing %s in %r', suffix, archive)

    with TemporaryDirectory() as folder:
        log.info('using temporary directory %r', folder)
        folder = resolve(folder)

        with tarfile.open(archive, 'r') as tarball:
            log.debug('extracting %r to %r', tarball.name, folder)
            tarball.extractall(folder, filter=lambda info, _: info if info.name.endswith(suffix) else None)

        yield from walk_dir(folder, suffix=suffix)


PACKAGE_RE = re.compile(r'Package: (?P<package>.+)$', re.MULTILINE)
VERSION_RE = re.compile(r'Version: (?P<version>.+)$', re.MULTILINE)
SIZE_RE = re.compile(r'Installed-Size: (?P<size>.+)$', re.MULTILINE)
DEPENDS_RE = re.compile(r'Depends: (?P<depends>.+)$', re.MULTILINE)
SUGGESTS_RE = re.compile(r'Suggests: (?P<suggests>.+)$', re.MULTILINE)
ENHANCES_RE = re.compile(r'Enhances: (?P<enhances>.+)$', re.MULTILINE)
PROVIDES_RE = re.compile(r'Provides: (?P<provides>.+)$', re.MULTILINE)
SECTION_RE = re.compile(r'Section: (?P<section>.+)$', re.MULTILINE)
PRIORITY_RE = re.compile(r'Priority: (?P<priority>.+)$', re.MULTILINE)
DESCRIPTION_RE = re.compile(r'Description:(?P<description>.*)$', re.DOTALL)


def match_group(text: str, pattern: re.Pattern[str], group: str, log: Logger) -> str:
    match = pattern.search(text)
    log.debug('%s = %s', group, match)
    assert match, f'Missing {group}: {text!r}'
    result = match.group(group)
    assert isinstance(result, str)
    return result.strip()


def match_list(text: str, pattern: re.Pattern[str], group: str, log: Logger) -> tuple[str, ...]:
    try:
        result = match_group(text, pattern, group, log)
    except AssertionError as error:
        log.debug('no %s', group, exc_info=error)
        result = ''

    if not result:
        return ()

    log.debug('matching %s: %r', group, result)
    items = list[str]()
    for entry in result.split(','):
        entry = entry.strip().split()
        log.debug('matching %s: %r', group, entry)
        items.append(entry[0])

    return tuple(items)


@dataclass(frozen=True)
class DebInfo:
    package: str
    version: str
    size: int
    depends: tuple[str, ...]
    suggests: tuple[str, ...]
    enhances: tuple[str, ...]
    provides: tuple[str, ...]
    section: str
    priority: str
    description: str

    @staticmethod
    def parse(control: str) -> DebInfo:
        log = logger('parse')
        log.debug('control line = %r', control)

        package = match_group(control, PACKAGE_RE, 'package', log)
        version = match_group(control, VERSION_RE, 'version', log)
        size = int(match_group(control, SIZE_RE, 'size', log))
        depends = match_list(control, DEPENDS_RE, 'depends', log)
        suggests = match_list(control, SUGGESTS_RE, 'suggests', log)
        enhances = match_list(control, ENHANCES_RE, 'enhances', log)
        provides = match_list(control, PROVIDES_RE, 'provides', log)
        section = match_group(control, SECTION_RE, 'section', log)
        priority = match_group(control, PRIORITY_RE, 'priority', log)
        description = match_group(control, DESCRIPTION_RE, 'description', log)

        return DebInfo(
            package=package,
            version=version,
            size=size,
            depends=depends,
            suggests=suggests,
            enhances=enhances,
            provides=provides,
            section=section,
            priority=priority,
            description=description,
        )


def extract_info(deb: Path) -> DebInfo:
    log = logger('extract_info')
    log.info('from %r', deb.name)
    log.debug('path = %r', deb)

    dpkg = Dpkg(str(deb), logger=log.getChild('pydpkg'))
    return DebInfo.parse(dpkg.control_str)


def extract_repo(repo: Path) -> Iterator[DebInfo]:
    log = logger('extract_repo')
    log.debug('from %r', repo.name)

    if repo.is_dir():
        log.info('undesrtood as directory: %r', repo.name)
        for deb in walk_dir(repo, suffix='.deb'):
            yield extract_info(deb)

    elif repo.suffix == '.deb':
        log.info('undesrtood as package: %r', repo.name)
        yield extract_info(repo)

    else:
        log.info('undesrtood as tarball: %r', repo.name)
        for deb in extract_tar(repo, suffix='.deb'):
            yield extract_info(deb)


def explore(repos: list[Path]) -> Iterator[DebInfo]:
    log = logger('explore')
    log.debug('repos: %r', repos)

    for repo in repos:
        yield from extract_repo(repo)


def main() -> None:
    parser = ArgumentParser(description='Graph depencies of local .deb packages')
    parser.add_argument('repo', nargs='+', help='Directory or tar to explore')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('-n', '--nodes', action='store_true')
    parser.add_argument('-e', '--edges', action='store_true')

    log = logger('main')
    log.debug('parsing arguments')
    args = parser.parse_intermixed_args()

    log.debug('verbosity: %s', args.verbose)
    set_verbosity(args.verbose)

    nodes = dict[str, DebInfo]()
    edges = dict[tuple[str, str], Literal['depends', 'suggests', 'enhances', 'provided']]()
    for deb in explore([resolve(path) for path in args.repo]):
        nodes[deb.package] = deb
        for dependency in deb.depends:
            edges[deb.package, dependency] = 'depends'
        for dependency in deb.suggests:
            edges[deb.package, dependency] = 'suggests'
        for dependency in deb.enhances:
            edges[deb.package, dependency] = 'enhances'
        for dependency in deb.provides:
            edges[dependency, deb.package] = 'provided'

    if args.nodes:
        print('id', 'shared name', 'version', 'section', 'priority', 'size', 'description', sep=',')
        for name, node in nodes.items():
            print(name, node.package, node.version, node.section, node.priority, node.size, repr(node.description), sep=',')

    if args.edges:
        print('source', 'target', 'interaction', sep=',')
        for (source, target), interaction in edges.items():
            print(source, target, interaction, sep=',')


if __name__ == '__main__':
    main()
