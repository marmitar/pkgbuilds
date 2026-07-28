# Personal PKGBUILDs

## AUR

<!-- > $
export PRINTSRCINFO=1
git submodule --quiet foreach "
  if git remote get-url origin | grep -qF 'ssh://aur@aur.archlinux.org/'; then
    version=\$(bash -c '. PKGBUILD; printf \"\${epoch/%?/&:}\${pkgver}-\${pkgrel}\"')
    printf '%s [%s %s](https://aur.archlinux.org/packages/%s)\n' - \
      \"\${displaypath}\" \"\${version}\" \"\${displaypath}\"
  fi
"
-->

<!-- BEGIN mdsh -->
- [alpaca-ai 9.2.4-1](https://aur.archlinux.org/packages/alpaca-ai)
- [esound 0.2.41-7](https://aur.archlinux.org/packages/esound)
- [intel-sgx-psw-bin 2.29-1](https://aur.archlinux.org/packages/intel-sgx-psw-bin)
- [intel-sgx-sdk-bin 2.29-1](https://aur.archlinux.org/packages/intel-sgx-sdk-bin)
- [licensecheck 3.3.10-1](https://aur.archlinux.org/packages/licensecheck)
- [mathematica 15.0.1-1](https://aur.archlinux.org/packages/mathematica)
- [mathematica-light 15.0.1-1](https://aur.archlinux.org/packages/mathematica-light)
- [pam_mount-git 2.22.r7.g78787d2-1](https://aur.archlinux.org/packages/pam_mount-git)
- [perl-feature-compat-class 0.08-1](https://aur.archlinux.org/packages/perl-feature-compat-class)
- [perl-feature-compat-try 0.05-3](https://aur.archlinux.org/packages/perl-feature-compat-try)
- [perl-log-any 1.720-1](https://aur.archlinux.org/packages/perl-log-any)
- [perl-string-escape 2010.002-4](https://aur.archlinux.org/packages/perl-string-escape)
- [perl-string-license 0.0.11-1](https://aur.archlinux.org/packages/perl-string-license)
- [perl-struct-dumb 0.16-1](https://aur.archlinux.org/packages/perl-struct-dumb)
- [perl-test-future-io-impl 0.21-1](https://aur.archlinux.org/packages/perl-test-future-io-impl)
- [perl-test2-tools-command 0.20-2](https://aur.archlinux.org/packages/perl-test2-tools-command)
- [perl-tree-rb-xs 0.21-1](https://aur.archlinux.org/packages/perl-tree-rb-xs)
- [physlock 13-5](https://aur.archlinux.org/packages/physlock)
- [pnpm-shell-completion 0.5.5-2](https://aur.archlinux.org/packages/pnpm-shell-completion)
- [python-cohere 7.0.8-1](https://aur.archlinux.org/packages/python-cohere)
- [python-funk 0.5.0.r12.gc9415c2-1](https://aur.archlinux.org/packages/python-funk)
- [python-speechrecognition 3.17.0-1](https://aur.archlinux.org/packages/python-speechrecognition)
- [shellcheck-bin-doc 0.11.0-1](https://aur.archlinux.org/packages/shellcheck-bin-doc)
- [tela-circle-icon-theme-spl-git 2026.07.07.r0.gc0adf1ab-1](https://aur.archlinux.org/packages/tela-circle-icon-theme-spl-git)
- [vkbasalt-redemp-git r470.gd5c38ed-1](https://aur.archlinux.org/packages/vkbasalt-redemp-git)
- [vscode-xdg-patch-hook 1.0.5-1](https://aur.archlinux.org/packages/vscode-xdg-patch-hook)
- [xpadneo-dkms 0.10.4-1](https://aur.archlinux.org/packages/xpadneo-dkms)
<!-- END mdsh -->

## Custom patches

<!-- > $
export PRINTSRCINFO=1
git submodule --quiet foreach "
  if ! git remote get-url origin | grep -qF 'ssh://aur@aur.archlinux.org/'; then
    version=\$(bash -c '. PKGBUILD; printf \"\${epoch/%?/&:}\${pkgver}-\${pkgrel}\"')
    printf '%s [%s %s](%s)\n' - \
      \"\${displaypath}\" \"\${version}\" \"\$(git remote get-url origin)\"

    series=\"../.patches/\${displaypath}/.series\"
    if [ ! -f \"\${series}\" ]; then
      exit
    fi

    while read -r patch; do
      printf '  1. [%s](.patches/%s/%s)\n' \
        \"\${patch}\" \"\${displaypath}\" \"\${patch}\"
    done < \"\${series}\"
  fi
"
-->

<!-- BEGIN mdsh -->
- [chezmoi 2.71.1-1](https://gitlab.archlinux.org/archlinux/packaging/packages/chezmoi.git)
  1. [get-latest-version.patch](.patches/chezmoi/get-latest-version.patch)
  1. [use-sprout-sprigin.patch](.patches/chezmoi/use-sprout-sprigin.patch)
  1. [fix-keys-with-dots.patch](.patches/chezmoi/fix-keys-with-dots.patch)
  1. [fix-empty-derivePassword.patch](.patches/chezmoi/fix-empty-derivePassword.patch)
- [thelounge-beta 4.6.0pre.1-1](https://aur.archlinux.org/thelounge-beta.git)
  1. [build-from-source.patch](.patches/thelounge-beta/build-from-source.patch)
  1. [update-dependencies.patch](.patches/thelounge-beta/update-dependencies.patch)
  1. [update-dependencies-wip.patch](.patches/thelounge-beta/update-dependencies-wip.patch)
<!-- END mdsh -->