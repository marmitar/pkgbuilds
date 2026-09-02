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
    pkgname=$(git show "${sha1}":.SRCINFO | sed -nE "/^\s*pkgname\s*=/ { s/.*=\s*(.*)$/\1/ p; q }")
    if [ -n "${epoch}" ]; then
      version="${epoch}:${pkgver}-${pkgrel}"
    else
      version="${pkgver}-${pkgrel}"
    fi

    maintainer="![AUR Maintainer](https://img.shields.io/aur/maintainer/${pkgname})"
    modified="![AUR Last Modified](https://img.shields.io/aur/last-modified/${pkgname})"
    license="![AUR License](https://img.shields.io/aur/license/${pkgname})"
    badges=$(printf "  %s\n" "${maintainer}" "${modified}" "${license}")
    printf "%s\n" "- \`${pkgbase} ${version}\` [[AUR](${url})] <br/>" "${badges}"
  fi
'
-->

<!-- BEGIN mdsh -->
- `alpaca-ai 9.2.5-1` [[AUR](https://aur.archlinux.org/pkgbase/alpaca-ai)] <br/>
  ![AUR Maintainer](https://img.shields.io/aur/maintainer/alpaca-ai)
  ![AUR Last Modified](https://img.shields.io/aur/last-modified/alpaca-ai)
  ![AUR License](https://img.shields.io/aur/license/alpaca-ai)
- `compressonator-git 4.5.52.r21.gf4b53d79-1` [[AUR](https://aur.archlinux.org/pkgbase/compressonator-git)] <br/>
  ![AUR Maintainer](https://img.shields.io/aur/maintainer/compressonator-git)
  ![AUR Last Modified](https://img.shields.io/aur/last-modified/compressonator-git)
  ![AUR License](https://img.shields.io/aur/license/compressonator-git)
- `esound 0.2.41-8` [[AUR](https://aur.archlinux.org/pkgbase/esound)] <br/>
  ![AUR Maintainer](https://img.shields.io/aur/maintainer/esound)
  ![AUR Last Modified](https://img.shields.io/aur/last-modified/esound)
  ![AUR License](https://img.shields.io/aur/license/esound)
- `hunk 0.20.1-1` [[AUR](https://aur.archlinux.org/pkgbase/hunk)] <br/>
  ![AUR Maintainer](https://img.shields.io/aur/maintainer/hunk)
  ![AUR Last Modified](https://img.shields.io/aur/last-modified/hunk)
  ![AUR License](https://img.shields.io/aur/license/hunk)
- `intel-sgx-psw-bin 2.30.1-1` [[AUR](https://aur.archlinux.org/pkgbase/intel-sgx-psw-bin)] <br/>
  ![AUR Maintainer](https://img.shields.io/aur/maintainer/intel-sgx-psw-bin)
  ![AUR Last Modified](https://img.shields.io/aur/last-modified/intel-sgx-psw-bin)
  ![AUR License](https://img.shields.io/aur/license/intel-sgx-psw-bin)
- `intel-sgx-sdk-bin 2.30.1-1` [[AUR](https://aur.archlinux.org/pkgbase/intel-sgx-sdk-bin)] <br/>
  ![AUR Maintainer](https://img.shields.io/aur/maintainer/intel-sgx-sdk-bin)
  ![AUR Last Modified](https://img.shields.io/aur/last-modified/intel-sgx-sdk-bin)
  ![AUR License](https://img.shields.io/aur/license/intel-sgx-sdk-bin)
- `licensecheck 3.3.10-1` [[AUR](https://aur.archlinux.org/pkgbase/licensecheck)] <br/>
  ![AUR Maintainer](https://img.shields.io/aur/maintainer/licensecheck)
  ![AUR Last Modified](https://img.shields.io/aur/last-modified/licensecheck)
  ![AUR License](https://img.shields.io/aur/license/licensecheck)
- `mathematica 15.0.1-1` [[AUR](https://aur.archlinux.org/pkgbase/mathematica)] <br/>
  ![AUR Maintainer](https://img.shields.io/aur/maintainer/mathematica)
  ![AUR Last Modified](https://img.shields.io/aur/last-modified/mathematica)
  ![AUR License](https://img.shields.io/aur/license/mathematica)
- `mathematica-light 15.0.1-1` [[AUR](https://aur.archlinux.org/pkgbase/mathematica-light)] <br/>
  ![AUR Maintainer](https://img.shields.io/aur/maintainer/mathematica-light)
  ![AUR Last Modified](https://img.shields.io/aur/last-modified/mathematica-light)
  ![AUR License](https://img.shields.io/aur/license/mathematica-light)
- `pam_mount-git 2.22.r7.g78787d2-2` [[AUR](https://aur.archlinux.org/pkgbase/pam_mount-git)] <br/>
  ![AUR Maintainer](https://img.shields.io/aur/maintainer/pam_mount-git)
  ![AUR Last Modified](https://img.shields.io/aur/last-modified/pam_mount-git)
  ![AUR License](https://img.shields.io/aur/license/pam_mount-git)
- `perl-feature-compat-class 0.08-1` [[AUR](https://aur.archlinux.org/pkgbase/perl-feature-compat-class)] <br/>
  ![AUR Maintainer](https://img.shields.io/aur/maintainer/perl-feature-compat-class)
  ![AUR Last Modified](https://img.shields.io/aur/last-modified/perl-feature-compat-class)
  ![AUR License](https://img.shields.io/aur/license/perl-feature-compat-class)
- `perl-feature-compat-try 0.05-3` [[AUR](https://aur.archlinux.org/pkgbase/perl-feature-compat-try)] <br/>
  ![AUR Maintainer](https://img.shields.io/aur/maintainer/perl-feature-compat-try)
  ![AUR Last Modified](https://img.shields.io/aur/last-modified/perl-feature-compat-try)
  ![AUR License](https://img.shields.io/aur/license/perl-feature-compat-try)
- `perl-log-any 1.720-1` [[AUR](https://aur.archlinux.org/pkgbase/perl-log-any)] <br/>
  ![AUR Maintainer](https://img.shields.io/aur/maintainer/perl-log-any)
  ![AUR Last Modified](https://img.shields.io/aur/last-modified/perl-log-any)
  ![AUR License](https://img.shields.io/aur/license/perl-log-any)
- `perl-string-escape 2010.002-4` [[AUR](https://aur.archlinux.org/pkgbase/perl-string-escape)] <br/>
  ![AUR Maintainer](https://img.shields.io/aur/maintainer/perl-string-escape)
  ![AUR Last Modified](https://img.shields.io/aur/last-modified/perl-string-escape)
  ![AUR License](https://img.shields.io/aur/license/perl-string-escape)
- `perl-string-license 0.0.11-1` [[AUR](https://aur.archlinux.org/pkgbase/perl-string-license)] <br/>
  ![AUR Maintainer](https://img.shields.io/aur/maintainer/perl-string-license)
  ![AUR Last Modified](https://img.shields.io/aur/last-modified/perl-string-license)
  ![AUR License](https://img.shields.io/aur/license/perl-string-license)
- `perl-struct-dumb 0.16-1` [[AUR](https://aur.archlinux.org/pkgbase/perl-struct-dumb)] <br/>
  ![AUR Maintainer](https://img.shields.io/aur/maintainer/perl-struct-dumb)
  ![AUR Last Modified](https://img.shields.io/aur/last-modified/perl-struct-dumb)
  ![AUR License](https://img.shields.io/aur/license/perl-struct-dumb)
- `perl-test-future-io-impl 0.21-1` [[AUR](https://aur.archlinux.org/pkgbase/perl-test-future-io-impl)] <br/>
  ![AUR Maintainer](https://img.shields.io/aur/maintainer/perl-test-future-io-impl)
  ![AUR Last Modified](https://img.shields.io/aur/last-modified/perl-test-future-io-impl)
  ![AUR License](https://img.shields.io/aur/license/perl-test-future-io-impl)
- `perl-test2-tools-command 0.20-2` [[AUR](https://aur.archlinux.org/pkgbase/perl-test2-tools-command)] <br/>
  ![AUR Maintainer](https://img.shields.io/aur/maintainer/perl-test2-tools-command)
  ![AUR Last Modified](https://img.shields.io/aur/last-modified/perl-test2-tools-command)
  ![AUR License](https://img.shields.io/aur/license/perl-test2-tools-command)
- `perl-tree-rb-xs 0.21-1` [[AUR](https://aur.archlinux.org/pkgbase/perl-tree-rb-xs)] <br/>
  ![AUR Maintainer](https://img.shields.io/aur/maintainer/perl-tree-rb-xs)
  ![AUR Last Modified](https://img.shields.io/aur/last-modified/perl-tree-rb-xs)
  ![AUR License](https://img.shields.io/aur/license/perl-tree-rb-xs)
- `physlock 13-5` [[AUR](https://aur.archlinux.org/pkgbase/physlock)] <br/>
  ![AUR Maintainer](https://img.shields.io/aur/maintainer/physlock)
  ![AUR Last Modified](https://img.shields.io/aur/last-modified/physlock)
  ![AUR License](https://img.shields.io/aur/license/physlock)
- `pnpm-shell-completion 0.5.5-2` [[AUR](https://aur.archlinux.org/pkgbase/pnpm-shell-completion)] <br/>
  ![AUR Maintainer](https://img.shields.io/aur/maintainer/pnpm-shell-completion)
  ![AUR Last Modified](https://img.shields.io/aur/last-modified/pnpm-shell-completion)
  ![AUR License](https://img.shields.io/aur/license/pnpm-shell-completion)
- `python-bencode2 0.3.33-2` [[AUR](https://aur.archlinux.org/pkgbase/python-bencode2)] <br/>
  ![AUR Maintainer](https://img.shields.io/aur/maintainer/python-bencode2)
  ![AUR Last Modified](https://img.shields.io/aur/last-modified/python-bencode2)
  ![AUR License](https://img.shields.io/aur/license/python-bencode2)
- `python-cohere 7.1.0-1` [[AUR](https://aur.archlinux.org/pkgbase/python-cohere)] <br/>
  ![AUR Maintainer](https://img.shields.io/aur/maintainer/python-cohere)
  ![AUR Last Modified](https://img.shields.io/aur/last-modified/python-cohere)
  ![AUR License](https://img.shields.io/aur/license/python-cohere)
- `python-funk 0.5.0.r12.gc9415c2-1` [[AUR](https://aur.archlinux.org/pkgbase/python-funk)] <br/>
  ![AUR Maintainer](https://img.shields.io/aur/maintainer/python-funk)
  ![AUR Last Modified](https://img.shields.io/aur/last-modified/python-funk)
  ![AUR License](https://img.shields.io/aur/license/python-funk)
- `python-speechrecognition 3.17.0-1` [[AUR](https://aur.archlinux.org/pkgbase/python-speechrecognition)] <br/>
  ![AUR Maintainer](https://img.shields.io/aur/maintainer/python-speechrecognition)
  ![AUR Last Modified](https://img.shields.io/aur/last-modified/python-speechrecognition)
  ![AUR License](https://img.shields.io/aur/license/python-speechrecognition)
- `shellcheck-bin-doc 0.11.0-1` [[AUR](https://aur.archlinux.org/pkgbase/shellcheck-bin-doc)] <br/>
  ![AUR Maintainer](https://img.shields.io/aur/maintainer/shellcheck-bin-doc)
  ![AUR Last Modified](https://img.shields.io/aur/last-modified/shellcheck-bin-doc)
  ![AUR License](https://img.shields.io/aur/license/shellcheck-bin-doc)
- `tela-circle-icon-theme-spl-git 2026.07.07.r12.gee3cf47b-1` [[AUR](https://aur.archlinux.org/pkgbase/tela-circle-icon-theme-spl-git)] <br/>
  ![AUR Maintainer](https://img.shields.io/aur/maintainer/tela-circle-icon-theme-all-git)
  ![AUR Last Modified](https://img.shields.io/aur/last-modified/tela-circle-icon-theme-all-git)
  ![AUR License](https://img.shields.io/aur/license/tela-circle-icon-theme-all-git)
- `vkbasalt-redemp-git r470.gd5c38ed-1` [[AUR](https://aur.archlinux.org/pkgbase/vkbasalt-redemp-git)] <br/>
  ![AUR Maintainer](https://img.shields.io/aur/maintainer/vkbasalt-redemp-git)
  ![AUR Last Modified](https://img.shields.io/aur/last-modified/vkbasalt-redemp-git)
  ![AUR License](https://img.shields.io/aur/license/vkbasalt-redemp-git)
- `xpadneo-dkms 0.10.4-1` [[AUR](https://aur.archlinux.org/pkgbase/xpadneo-dkms)] <br/>
  ![AUR Maintainer](https://img.shields.io/aur/maintainer/xpadneo-dkms)
  ![AUR Last Modified](https://img.shields.io/aur/last-modified/xpadneo-dkms)
  ![AUR License](https://img.shields.io/aur/license/xpadneo-dkms)
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
    pkgname=$(git show "${sha1}":.SRCINFO | sed -nE "/^\s*pkgname\s*=/ { s/.*=\s*(.*)$/\1/ p; q }")
    if [ -n "${epoch}" ]; then
      version="${epoch}:${pkgver}-${pkgrel}"
    else
      version="${pkgver}-${pkgrel}"
    fi

    case "${url}" in
      "https://aur.archlinux.org/"*)
        badge="![AUR Version](https://img.shields.io/aur/version/${pkgname})"
        ;;
      "https://gitlab.archlinux.org/"*)
        gitlab=$(perl -MURI::Escape -e "print uri_escape(@ARGV[0])" "https://gitlab.archlinux.org")
        project=$(perl -MURI -MURI::Escape -e "print uri_escape(URI->new(@ARGV[0])->path =~ s/^\///r)" "${url}")
        badge="![GitLab Tag](https://img.shields.io/gitlab/v/tag/${project}?gitlab_url=${gitlab})"
        ;;
      *)
        badge="![Static Badge](https://img.shields.io/badge/source-unknown-red)"
        ;;
    esac
    printf "%s\n" "- \`${pkgbase} ${version}\` [[upstream](${url})]" "  ${badge}"

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
- `chezmoi 2.72.0-1` [[upstream](https://gitlab.archlinux.org/archlinux/packaging/packages/chezmoi)]
  ![GitLab Tag](https://img.shields.io/gitlab/v/tag/archlinux%2Fpackaging%2Fpackages%2Fchezmoi?gitlab_url=https%3A%2F%2Fgitlab.archlinux.org)
  1. [`get-latest-version.patch`](.patches/chezmoi/get-latest-version.patch)
  1. [`use-sprout-sprigin.patch`](.patches/chezmoi/use-sprout-sprigin.patch)
  1. [`fix-empty-derivePassword.patch`](.patches/chezmoi/fix-empty-derivePassword.patch)
- `thelounge-beta 4.6.0pre.1-1` [[upstream](https://aur.archlinux.org/pkgbase/thelounge-beta)]
  ![AUR Version](https://img.shields.io/aur/version/thelounge-beta)
  1. [`build-from-source.patch`](.patches/thelounge-beta/build-from-source.patch)
  1. [`update-dependencies.patch`](.patches/thelounge-beta/update-dependencies.patch)
  1. [`update-dependencies-wip.patch`](.patches/thelounge-beta/update-dependencies-wip.patch)
<!-- END mdsh -->
