# Personal PKGBUILDs

## AUR

<!-- > $
git submodule --quiet foreach '
  if git remote get-url origin | grep -qF "ssh://aur@aur.archlinux.org/"; then
    pkgbase="${displaypath}"
    url="https://aur.archlinux.org/pkgbase/${pkgbase}"
    epoch=$(git show "${sha1}":.SRCINFO | sed -nE "s/^\s*epoch\s*=\s*(.*)$/\1/ p")
    pkgver=$(git show "${sha1}":.SRCINFO | sed -nE "s/^\s*pkgver\s*=\s*(.*)$/\1/ p")
    pkgrel=$(git show "${sha1}":.SRCINFO | sed -nE "s/^\s*pkgrel\s*=\s*(.*)$/\1/ p")
    if [ -n "${epoch}" ]; then
      version="${epoch}:${pkgver}-${pkgrel}"
    else
      version="${pkgver}-${pkgrel}"
    fi

    printf "%s \`%s\` %s [[AUR](%s)]\n" - "${pkgbase}" "${version}" "${url}"
  fi
'
-->

<!-- BEGIN mdsh -->
- `alpaca-ai` 9.2.4-1 [[AUR](https://aur.archlinux.org/pkgbase/alpaca-ai)]
- `esound` 0.2.41-7 [[AUR](https://aur.archlinux.org/pkgbase/esound)]
- `hunk` 0.17.7-2 [[AUR](https://aur.archlinux.org/pkgbase/hunk)]
- `intel-sgx-psw-bin` 2.30-1 [[AUR](https://aur.archlinux.org/pkgbase/intel-sgx-psw-bin)]
- `intel-sgx-sdk-bin` 2.30-1 [[AUR](https://aur.archlinux.org/pkgbase/intel-sgx-sdk-bin)]
- `licensecheck` 3.3.10-1 [[AUR](https://aur.archlinux.org/pkgbase/licensecheck)]
- `mathematica` 15.0.1-1 [[AUR](https://aur.archlinux.org/pkgbase/mathematica)]
- `mathematica-light` 15.0.1-1 [[AUR](https://aur.archlinux.org/pkgbase/mathematica-light)]
- `pam_mount-git` 2.22.r7.g78787d2-1 [[AUR](https://aur.archlinux.org/pkgbase/pam_mount-git)]
- `perl-feature-compat-class` 0.08-1 [[AUR](https://aur.archlinux.org/pkgbase/perl-feature-compat-class)]
- `perl-feature-compat-try` 0.05-3 [[AUR](https://aur.archlinux.org/pkgbase/perl-feature-compat-try)]
- `perl-log-any` 1.720-1 [[AUR](https://aur.archlinux.org/pkgbase/perl-log-any)]
- `perl-string-escape` 2010.002-4 [[AUR](https://aur.archlinux.org/pkgbase/perl-string-escape)]
- `perl-string-license` 0.0.11-1 [[AUR](https://aur.archlinux.org/pkgbase/perl-string-license)]
- `perl-struct-dumb` 0.16-1 [[AUR](https://aur.archlinux.org/pkgbase/perl-struct-dumb)]
- `perl-test-future-io-impl` 0.21-1 [[AUR](https://aur.archlinux.org/pkgbase/perl-test-future-io-impl)]
- `perl-test2-tools-command` 0.20-2 [[AUR](https://aur.archlinux.org/pkgbase/perl-test2-tools-command)]
- `perl-tree-rb-xs` 0.21-1 [[AUR](https://aur.archlinux.org/pkgbase/perl-tree-rb-xs)]
- `physlock` 13-5 [[AUR](https://aur.archlinux.org/pkgbase/physlock)]
- `pnpm-shell-completion` 0.5.5-2 [[AUR](https://aur.archlinux.org/pkgbase/pnpm-shell-completion)]
- `python-cohere` 7.0.8-1 [[AUR](https://aur.archlinux.org/pkgbase/python-cohere)]
- `python-funk` 0.5.0.r12.gc9415c2-1 [[AUR](https://aur.archlinux.org/pkgbase/python-funk)]
- `python-speechrecognition` 3.17.0-1 [[AUR](https://aur.archlinux.org/pkgbase/python-speechrecognition)]
- `shellcheck-bin-doc` 0.11.0-1 [[AUR](https://aur.archlinux.org/pkgbase/shellcheck-bin-doc)]
- `tela-circle-icon-theme-spl-git` 2026.07.07.r0.gc0adf1ab-1 [[AUR](https://aur.archlinux.org/pkgbase/tela-circle-icon-theme-spl-git)]
- `vkbasalt-redemp-git` r470.gd5c38ed-1 [[AUR](https://aur.archlinux.org/pkgbase/vkbasalt-redemp-git)]
- `vscode-xdg-patch-hook` 1.0.5-1 [[AUR](https://aur.archlinux.org/pkgbase/vscode-xdg-patch-hook)]
- `xpadneo-dkms` 0.10.4-1 [[AUR](https://aur.archlinux.org/pkgbase/xpadneo-dkms)]
<!-- END mdsh -->

## Custom patches

<!-- > $
git submodule --quiet foreach '
  if ! git remote get-url origin | grep -qF "ssh://aur@aur.archlinux.org/"; then
    pkgbase=${displaypath}
    url=$(git remote get-url origin | sed -E "s/\.git//;s|(https://aur.archlinux.org)|\1/pkgbase|")
    epoch=$(git show "${sha1}":.SRCINFO | sed -nE "s/^\s*epoch\s*=\s*(.*)$/\1/ p")
    pkgver=$(git show "${sha1}":.SRCINFO | sed -nE "s/^\s*pkgver\s*=\s*(.*)$/\1/ p")
    pkgrel=$(git show "${sha1}":.SRCINFO | sed -nE "s/^\s*pkgrel\s*=\s*(.*)$/\1/ p")
    if [ -n "${epoch}" ]; then
      version="${epoch}:${pkgver}-${pkgrel}"
    else
      version="${pkgver}-${pkgrel}"
    fi

    printf "%s \`%s\` %s [[upstream](%s)]\n" - "${pkgbase}" "${version}" "${url}"

    series="../.patches/${displaypath}/.series"
    if [ ! -f "${series}" ]; then
      exit
    fi
    while read -r patch; do
      printf "  1. [\`%s\`](.patches/%s/%s)\n" "${patch}" "${displaypath}" "${patch}"
    done < "${series}"
  fi
'
-->

<!-- BEGIN mdsh -->
- `chezmoi` 2.71.1-1 [[upstream](https://gitlab.archlinux.org/archlinux/packaging/packages/chezmoi)]
  1. [`get-latest-version.patch`](.patches/chezmoi/get-latest-version.patch)
  1. [`use-sprout-sprigin.patch`](.patches/chezmoi/use-sprout-sprigin.patch)
  1. [`fix-keys-with-dots.patch`](.patches/chezmoi/fix-keys-with-dots.patch)
  1. [`fix-empty-derivePassword.patch`](.patches/chezmoi/fix-empty-derivePassword.patch)
- `thelounge-beta` 4.6.0pre.1-1 [[upstream](https://aur.archlinux.org/pkgbase/thelounge-beta)]
  1. [`build-from-source.patch`](.patches/thelounge-beta/build-from-source.patch)
  1. [`update-dependencies.patch`](.patches/thelounge-beta/update-dependencies.patch)
  1. [`update-dependencies-wip.patch`](.patches/thelounge-beta/update-dependencies-wip.patch)
<!-- END mdsh -->
