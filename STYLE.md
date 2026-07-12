# PKGBUILD Style

Somewhat based on <https://man.archlinux.org/man/PKGBUILD.5>.

## Variables

- `pkgname`, `pkgver`, `pkgrel`, `epoch`, `install`, `changelog`: **unquoted**
- `pkgdesc`: preferably **single-quoted**
- `url`: always **single-quoted** (no string interpolation, easier to access)
- All arrays (except `arch` and `options`): **single-quoted elements**, double-quote only when interpolating
- `arch`: **unquoted** (based on [alpm-lint][systemarchitecture] and [RFC 32][rfc0032])
- `options`: **unquoted** (similar to `OPTIONS` in [`makepkg.conf`][makepkg-conf])

In general:

1. **unquoted** for strings that cannot have spaces in them (package names, versions, etc.)
2. **single-quoted** for static strings that may have spaces (including dependencies, which can contains complex version
   requirements with spaces)
3. **double-quoted** for all interpolations, so it's clear these strings depend on other strings
4. mixed **quoted** and **unquoted** for globbing, if necessary

I try to sort them like `.SRCINFO`, but in some cases (e.g. with variable references), it might work better in another
ordering.

## Commands

No unnecessary `${srcdir}` usages. They just clutter strings and make it harder to review the PKGBUILD.

For `install` and `ln`, I tend to favor:

1. `install -vD -t DIRECTORY/ -m644 FILES...` (note: basenames only)
2. `install -vD -m755 FILE -T TARGET` (rename file)
3. `find dir/ -type f -exec install -vD -m644 '{}' -T "${DIRECTORY}/{}" \;` (keep folder structure)
4. `install -vd DIRECTORIES/...` (for commands that won't create the directories themselves)

To avoid prompts, use `patch -t -Npx -i PATCH` or `patch -t -d DIR/ -Npx < PATCH`.

## See also

- [.editorconfig](./.editorconfig) (with [shfmt](https://github.com/mvdan/sh) options)
- [.shellcheckrc](./.shellcheckrc)

# Patches

Follow the [Debian Enhancement Proposal 3](https://dep-team.pages.debian.net/deps/dep3/).

[makepkg-conf]: https://man.archlinux.org/man/core/pacman/makepkg.conf.5.en
[rfc0032]: https://rfc.archlinux.page/0032-arch-linux-ports/
[systemarchitecture]: https://gitlab.archlinux.org/archlinux/alpm/alpm/-/blob/f61d0ef717c40695c387ce0199658695c9422a7e/alpm-types/src/system.rs#L66
