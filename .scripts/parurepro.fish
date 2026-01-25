#!/usr/bin/fish

function deactivate --description 'Exit virtualenv mode and return to the normal environment.'
    # reset old environment variables
    if test -n "$_OLD_VIRTUAL_PATH"
        # https://github.com/fish-shell/fish-shell/issues/436 altered PATH handling
        if test (string sub -s 1 -l 1 $FISH_VERSION) -lt 3
            set -gx PATH (_fishify_path "$_OLD_VIRTUAL_PATH")
        else
            set -gx PATH $_OLD_VIRTUAL_PATH
        end
        set -e _OLD_VIRTUAL_PATH
    end

    if test -n "$_OLD_VIRTUAL_PYTHONHOME"
        set -gx PYTHONHOME "$_OLD_VIRTUAL_PYTHONHOME"
        set -e _OLD_VIRTUAL_PYTHONHOME
    end

    if test -n "$_OLD_FISH_PROMPT_OVERRIDE"
       and functions -q _old_fish_prompt
        # Set an empty local `$fish_function_path` to allow the removal of `fish_prompt` using `functions -e`.
        set -l fish_function_path

        # Erase virtualenv's `fish_prompt` and restore the original.
        functions -e fish_prompt
        functions -c _old_fish_prompt fish_prompt
        functions -e _old_fish_prompt
        set -e _OLD_FISH_PROMPT_OVERRIDE
    end

    set -e VIRTUAL_ENV
    set -e VIRTUAL_ENV_PROMPT

    if test "$argv[1]" != 'nondestructive'
        # Self-destruct!
        functions -e pydoc
        functions -e deactivate
        functions -e _bashify_path
        functions -e _fishify_path
    end
end

argparse --move-unknown 't/timestamp=&' -- $argv
or return 1

if test -z "$_flag_timestamp"
    echo 'Missing --timestamp' > /dev/stderr
    return 1
end

set -l snapshot "$(date -u +'%Y/%m/%d' --date=@$_flag_timestamp)"
or return 1

set -l cfg "$(mktemp -d)"
chmod ugo+rx $cfg

function cleanup --inherit-variable cfg --on-process-exit $fish_pid --on-signal SIGINT
    rm -rf $cfg
end

printf 'Server = https://archive.archlinux.org/repos/%s/$repo/os/$arch' $snapshot > $cfg/mirrorlist
cat /etc/pacman.conf | string replace '/etc/pacman.d/mirrorlist' $cfg/mirrorlist > $cfg/pacman.conf
chmod ugo+r $cfg/{mirrorlist,pacman.conf}

printf '#!/bin/sh\nexec pacman-conf "$@" --config "%s"\n' $cfg/pacman.conf > $cfg/pacman-conf
chmod ugo+rx $cfg/pacman-conf

deactivate

# might need: sudo rm -rf /var/lib/aurbuild/x86_64
set -lx SOURCE_DATE_EPOCH $timestamp
command paru --config $cfg/pacman.conf --pacman-conf $cfg/pacman-conf $argv_opts $argv
