#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.14"
# dependencies = ["colorlog>=6.10.1"]
# ///

from argparse import ArgumentParser
from collections.abc import Iterator
from dataclasses import dataclass
from logging import Logger
from pathlib import Path


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
    relative = absolute.relative_to(CURRENT_DIRECTORY, walk_up=True)

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


def walk_tar(archive: Path, *, suffix: str) -> Iterator[Path]:
    import tarfile
    from tempfile import NamedTemporaryFile

    log = logger('walk_tar')
    log.debug('listing %s in %r', suffix, archive)

    with tarfile.open(archive, 'r') as tarball:
        for file in tarball:
            if not file.name.endswith(suffix):
                log.debug('not a %s file, ignored: %s :: %r', suffix, tarball.name, file.path)
                continue

            with NamedTemporaryFile(suffix=suffix) as temp:
                log.debug('extracting %r :: %r to %r', tarball.name, file.path, temp.name)
                tarball.extract(file, temp.name)

                yield Path(temp.name)


@dataclass(frozen=True)
class DebInfo:
    path: Path
    # TODO


def extract_info(deb: Path) -> DebInfo:
    log = logger('extract_info')
    log.info('from %r', deb.name)
    log.debug('path = %r', deb)

    return DebInfo(deb)


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
        for deb in walk_tar(repo, suffix='.deb'):
            yield extract_info(deb)


def explore(repos: list[Path]) -> Iterator[DebInfo]:
    log = logger('explore')
    log.debug('repos: %r', repos)

    for repo in repos:
        yield from extract_repo(repo)


def main() -> None:
    parser = ArgumentParser(description='Graph depencies of local .deb packages')
    parser.add_argument('repo', nargs='+', help='Directory or tar to explore')
    parser.add_argument('--verbose', '-v', action='count', default=0)

    log = logger('main')
    log.debug('parsing arguments')
    args = parser.parse_intermixed_args()

    log.debug('verbosity: %s', args.verbose)
    set_verbosity(args.verbose)

    for deb in explore([resolve(path) for path in args.repo]):
        print(deb.path)


if __name__ == '__main__':
    main()
