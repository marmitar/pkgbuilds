#!/usr/bin/fish
argparse --exclusive 'repo,package' '/repo' '/package' 'v/verbose' -- $argv
or return

set -l verbose
if test -n "$_flag_verbose"
    set verbose -v
end

function strip_extensions -a path
    while test -n "$path"
        set -l next (path change-extension '' $path)
        if test $next = $path
            echo $next
            return
        end
        set path $next
    end
end

function extract_package -a deb
    set -l name (dpkg-deb -I $deb | string replace -fr '^\s*Package:\s+(\S+)$' '$1')
    if test (count $name) -ne 1
        echo "Invalid deb file: $deb" >&2
        return 1
    end

    echo "==> Extracting $name..."
    mkdir -p $name
    dpkg-deb -I $deb > $name/INFO
    bsdtar -xf $deb -C $name $verbose
    for file in (fd -HI '\.tar(\.\S+)?$' $name)
        set -l target (strip_extensions $file)
        mkdir -p $target
        bsdtar -xf $file -C $target $verbose
        rm -f $file
    end
end

function extract_repo -a tar
    set -l root (bsdtar -tf $tar | string replace -r '^(\w+)/.*' '$1' | uniq)

    echo "==> Repository $tar:"
    bsdtar -xf $tar $verbose
    for dir in $root
        echo "==> Unpacking $dir"
        set -l packages (fd -HI '\.deb$' $dir)
        mkdir -p $dir/packages
        pushd $dir/packages
        for deb in $packages
            extract_package ../../$deb
        end
        popd
    end
end

for item in $argv
    if test -n "$_flag_repo"
        extract_repo $item
    else if test -n "$_flag_package"
        extract_package $item
    else
        echo 'Missing --repo or --package' >&2
        return 1
    end
end
