set lazy
set default-list

# Setup git hooks
configure-git:
    prek install
    git submodule update --init --recursive
    git submodule foreach --recursive \
        'prek install --config="$(realpath -e --relative-to="$(pwd)" "${toplevel}/.pre-commit-config.yaml")"'

submodule-root := shell('realpath -e --relative-to="${1}" "$(git -C "${2}" rev-parse --show-toplevel)"', justfile_directory(), invocation_directory())

# Check state of a single repository
[script]
@check submodule=submodule-root:
    cd {{ quote(submodule) }}
    toplevel={{ quote(justfile_directory()) }}
    prek run --all-files --config="${toplevel}/.pre-commit-config.yaml" {{
        if shell('git -C "${1}" remote get-url origin', submodule) =~ '^https?://' {
            '--dry-run'
        } else {
            ''
        }
    }}

# Check the state of all submodules
check-all:
    prek run --all-files --config='.pre-commit-config.yaml'
    git submodule foreach --recursive \
        'just check "${displaypath}" || :'

prek-version := `prek --version | awk '{print $2}'`

# Update .pre-commit-config.yaml
update-prek:
    prek auto-update --freeze --exclude-repo https://github.com/zimbatm/mdsh
    grep -qE '^minimum_prek_version:' .pre-commit-config.yaml
    sed -i -E "s/(minimum_prek_version:).*/\1 {{ prek-version }}/" .pre-commit-config.yaml

# List managed packages in README.md
update-readme:
    mdsh
