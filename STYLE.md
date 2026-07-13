# PKGBUILD Style

Somewhat based on <https://man.archlinux.org/man/PKGBUILD.5>.

## Variables

- `pkgname`, `pkgver`, `pkgrel`, `epoch`, `install`, `changelog`: **unquoted**
- `pkgdesc`: preferably **single-quoted**
- `url`: always **single-quoted**
- All arrays (except `arch` and `options`): **single-quoted elements**, double-quote only when interpolating
- `arch`: **unquoted** (based on [alpm-lint][systemarchitecture] and [RFC 32][rfc0032])
- `options`: **unquoted** (similar to `OPTIONS` in `makepkg.conf`)

## See also

- [.editorconfig](./.editorconfig) (with [shfmt](https://github.com/mvdan/sh) options)
- [.shellcheckrc](./.shellcheckrc)

# Patches

Follow the [Debian Enhancement Proposal 3](https://dep-team.pages.debian.net/deps/dep3/).

[rfc0032]: https://rfc.archlinux.page/0032-arch-linux-ports/
[systemarchitecture]: https://gitlab.archlinux.org/archlinux/alpm/alpm/-/blob/f61d0ef717c40695c387ce0199658695c9422a7e/alpm-types/src/system.rs#L66
