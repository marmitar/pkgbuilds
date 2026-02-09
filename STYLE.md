# PKGBUILD Style

Somewhat based on <https://man.archlinux.org/man/PKGBUILD.5>.

## Variables

- `pkgname`, `pkgver`, `pkgrel`, `epoch`, `install`, `changelog`: **unquoted**
- `pkgdesc`: preferrably **single-quoted**
- `url`: always **single-quoted**
- All arrays (except `options`): **single-quoted elements**, double-quote only when interpolating
- `options`: **unquoted tokens** (similar to `OPTIONS` in `makepkg.conf`)

## See also

- [.editorconfig](./.editorconfig) (with [shfmt](https://github.com/mvdan/sh) options)
- [.shellcheckrc](./.shellcheckrc)

# Patches

Follow the [Debian Enhancement Proposal 3](https://dep-team.pages.debian.net/deps/dep3/).
