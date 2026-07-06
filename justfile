set lazy
set default-list

prek-config := absolute_path('.pre-commit-config.yaml')

# Setup git hooks
configure-git:
    prek install
    git submodule init
    git submodule update --recursive
    git submodule foreach prek install --config {{ quote(prek-config) }}

submodule-root := shell('realpath --canonicalize-existing --relative-to="$2" "$(cd "$1" && git rev-parse --show-toplevel)"', invocation_directory(), justfile_directory())

# Check state of a single repository
check submodule=submodule-root:
    cd {{ quote(submodule) }} && prek run -a --config {{ quote(prek-config) }}

# Check the state of all submodules
check-all:
    prek run -a
    git submodule foreach sh -c 'prek run -a --config {{ quote(prek-config) }} || :'

prek-version := `prek --version | awk '{print $2}'`

# Update .pre-commit-config.yaml
update-prek:
    prek auto-update --freeze
    grep -qE '^minimum_prek_version:' .pre-commit-config.yaml
    sed -i -E "s/(minimum_prek_version:).*/\1 {{ prek-version }}/" .pre-commit-config.yaml
