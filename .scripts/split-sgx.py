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
from typing import Final, LiteralString

from pydpkg import Dpkg


GROUPS: Final[dict[LiteralString, frozenset[LiteralString]]] = {
    'intel-sgx-psw-common-bin': frozenset({
        'libsgx-enclave-common',
        'libsgx-enclave-common-dev',
        'libsgx-headers',
        'libsgx-launch',
        'libsgx-launch-dev',
        'libsgx-urts',
    }),
    'intel-sgx-aesm-bin': frozenset({
        'sgx-aesm-service',
        'libsgx-uae-service',
        'libsgx-ae-epid',
        'libsgx-ae-id-enclave',
        'libsgx-ae-le',
        'libsgx-ae-pce',
        'libsgx-ae-qe3',
        'libsgx-ae-qve',
        'libsgx-aesm-ecdsa-plugin',
        'libsgx-aesm-epid-plugin',
        'libsgx-aesm-launch-plugin',
        'libsgx-aesm-pce-plugin',
        'libsgx-aesm-quote-ex-plugin',
        'libsgx-qe3-logic',
        'libsgx-epid-dev',
        'libsgx-epid',
        'libsgx-pce-logic',
    }),
    'intel-sgx-ra-bin': frozenset({
        'sgx-ra-service',
        'libsgx-ra-network',
        'libsgx-ra-network-dev',
        'libsgx-ra-uefi',
        'libsgx-ra-uefi-dev',
    }),
    'intel-sgx-qgs-bin': frozenset({
        'tdx-qgs',
        'libsgx-tdx-logic',
        'libsgx-tdx-logic-dev',
        'libsgx-quote-ex',
        'libsgx-quote-ex-dev',
        'libsgx-ae-tdqe',
        'libtdx-attest',
        'libtdx-attest-dev',
    }),
    'intel-sgx-dcap-bin': frozenset({
        'sgx-dcap-pccs',
        'libsgx-dcap-ql',
        'libsgx-dcap-ql-dev',
        'libsgx-dcap-default-qpl',
        'libsgx-dcap-default-qpl-dev',
        'libsgx-dcap-quote-verify',
        'libsgx-dcap-quote-verify-dev',
        'intel-tee-pccs-admin-tool',
        'intel-tee-pcs-client-tool',
        'sgx-pck-id-retrieval-tool',
        'tee-appraisal-tool',
    }),
}


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
    log = logger('resolve')

    absolute = Path(path).resolve(strict=True)
    try:
        relative = absolute.relative_to(CURRENT_DIRECTORY)
        log.debug('path=%r to %r (%r)', path, relative, absolute)
    except ValueError as error:
        relative = absolute
        log.debug('path=%r (%r) not relative to %r', path, absolute, CURRENT_DIRECTORY, exc_info=error)

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
DESCRIPTION_RE = re.compile(r'Description:(?P<description>.*)$', re.MULTILINE)


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


@dataclass(frozen=True, slots=True)
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


def explore(*repos: Path) -> Iterator[DebInfo]:
    log = logger('explore')
    log.debug('repos: %r', repos)

    for repo in repos:
        yield from extract_repo(repo)


def root() -> Path:
    return resolve(__file__).parent.parent


def main() -> None:
    parser = ArgumentParser(description='Graph dependencies of local sgx_*_debian_local_repo')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('-i', '--internal', action='store_true')

    log = logger('main')
    log.debug('parsing arguments')
    args = parser.parse_intermixed_args()

    set_verbosity(args.verbose)
    log.debug('args: %s', args)
    repo = root() / 'intel-sgx-psw-bin' / 'sgx_2.27_debian_local_repo.tgz'

    groups = {name: set[DebInfo]() for name in GROUPS}
    loc = dict[str, str | None]()
    for deb in explore(repo):
        loc[deb.package] = None
        for group, packages in GROUPS.items():
            if deb.package in packages or deb.package.replace('-dbgsym', '') in packages:
                groups[group].add(deb)
                loc[deb.package] = group

    for group, packages in groups.items():
        print(f'============> {group}:')
        deps = set[str]()
        optdeps = set[str]()
        for deb in sorted(packages, key=lambda p: p.package):
            print()
            print(f'{deb.package}:')
            print(f'\t{deb.description}')
            edeps = [dep for dep in deb.depends if loc.get(dep) != group]
            deps.update(edeps)
            optdeps.update(dep for dep in deb.suggests if loc.get(dep) != group)
            optdeps.update(dep for dep in deb.enhances if loc.get(dep) != group)
            print(f'\tExternal dependencies: {edeps}')
            if args.internal:
                ideps = [dep for dep in deb.depends if loc.get(dep) == group]
                print(f'\tInternal dependencies: {ideps}')
        print()
        print(f'Total dependencies: {sorted(deps)}')
        print(f'Optional dependencies: {sorted(optdeps)}')
        print()

    for package, group in loc.items():
        if not group:
            log.warning('unhandled package: %s', package)


if __name__ == '__main__':
    main()
