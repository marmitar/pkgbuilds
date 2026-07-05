set lazy
set default-list

prek-config := absolute_path('.pre-commit-config.yaml')

# Setup git hooks
configure-git:
    prek install
    git submodule init
    git submodule update --recursive
    git submodule foreach prek install --config {{ quote(prek-config) }}

# Check state of a single repository
check submodule='.':
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
