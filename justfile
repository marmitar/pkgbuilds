set lazy
set default-list

# Setup git hooks
configure-git:
    prek install
    git submodule update --init --recursive
    git submodule foreach \
        'prek install --config="$(realpath -e --relative-to="$(pwd)" "${toplevel}/.pre-commit-config.yaml")"'

submodule-root := shell('realpath -e --relative-to="${1}" "$(git -C "${2}" rev-parse --show-toplevel)"', justfile_directory(), invocation_directory())

# Check state of a single repository
check submodule=submodule-root:
    cd {{ quote(submodule) }} && \
        prek run --all-files --config={{ quote(shell('realpath -e --relative-to="${1}" "${2}/.pre-commit-config.yaml"', submodule, justfile_directory())) }}

# Check the state of all submodules
check-all:
    prek run --all-files --config='.pre-commit-config.yaml'
    git submodule foreach \
        'prek run --all-files --config="${toplevel}/.pre-commit-config.yaml" || :'

prek-version := `prek --version | awk '{print $2}'`

# Update .pre-commit-config.yaml
update-prek:
    prek auto-update --freeze
    grep -qE '^minimum_prek_version:' .pre-commit-config.yaml
    sed -i -E "s/(minimum_prek_version:).*/\1 {{ prek-version }}/" .pre-commit-config.yaml
