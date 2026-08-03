#!/usr/bin/bash
# shellcheck disable=SC2312
set -euo pipefail

PACKAGE="${1:?missing package}"

rm -rf issues
mkdir -p issues

libdeps() {
  printf '%s\n' "$@" | awk '{print $4}' | awk -F'=' '{print $1}'
}

python_list() {
  LIST=$(rg --only-matching '\[[^\]]*\]' | head -n 1)
  python -c "print(*${LIST}, sep='\n')"
}

paren_list() {
  rg --only-matching '\([^)]*\)' | head -n 1 | sed -E 's/^\(|\)$//g' | sed -E 's/, /\n/g'
}

parse_dependency() {
  mkdir -p issues/DEPENDS
  KIND="$1"
  LINE="$2"

  NEEDED=$(printf '%s\n' "${LINE}" | awk '{print $5}' | sed -E 's/^\(//')
  printf '%s\n' "${LINE}" | case "${NEEDED}" in
    libraries-needed)
      # shellcheck disable=SC2046
      basename -a $(python_list) >> issues/DEPENDS/"soname-${KIND}".list
      ;;
    python-modules-needed)
      python_list >> issues/DEPENDS/"python-${KIND}".list
      ;;
    java-runtime-needed)
      paren_list | tail -n +2 >> issues/DEPENDS/"java-${KIND}".list
      ;;
    *)
      cat >> issues/DEPENDS/"unknown-${KIND}".list
      ;;
  esac
}

namcap --info --machine-readable "${PACKAGE}" | while IFS= read -r line; do
  # see /usr/share/namcap/namcap-tags
  TAG=$(awk '{print $3}' <<< "${line}")
  case "${TAG}" in
    elffile-* | insecure-r*path | unused-sodepend)
      # ELF files are provided from upstream
      continue
      ;;
    link-level-dependence | symlink-found)
      # we want other infos, but not these two
      continue
      ;;
    libdepends-detected-*)
      mkdir -p issues/LIBDEPENDS
      KIND="${TAG/#libdepends-detected-/}"
      # shellcheck disable=SC2046
      basename -a $(libdeps "${line}") >> issues/LIBDEPENDS/"soname-${KIND}".list
      ;;
    dependency-detected-*)
      KIND="${TAG/#dependency-detected-/}"
      parse_dependency "${KIND}" "${line}"
      ;;
    dependency-implicitly-*)
      KIND=implicitly
      parse_dependency "${KIND}" "${line}"
      ;;
    *) ;;
  esac
  printf '%s\n' "${line}" >> issues/"${TAG}.list"
done

check_sonames() {
  mapfile -t SONAMES < <(sort "$1" | uniq)

  echo > "$1"
  for soname in "${SONAMES[@]}"; do
    MATCHES=$(fd -HIs "${soname}" /opt/Mathematica | grep -E '.' || echo ❌)
    printf '%s\n' "${soname}" "${MATCHES}" >> "$1"
  done
}

for file in issues/*/soname-*.list; do
  check_sonames "${file}"
done

echo '## POSSIBLY MISSING DEPENDENCIES ##'
rg -F '❌' --no-filename issues/*/soname-*.list | awk '{print $1}' | sort | uniq
