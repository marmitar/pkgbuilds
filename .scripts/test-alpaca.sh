#!/usr/bin/sh
exec podman run --rm -it \
  -v "${XDG_RUNTIME_DIR}/${WAYLAND_DISPLAY}":/run/w0 \
  -e XDG_RUNTIME_DIR=/run \
  -e WAYLAND_DISPLAY=w0 \
  -e XDG_SESSION_TYPE=wayland \
  -e GDK_BACKEND=wayland \
  -v ./cache:/var/cache/pacman/pkg \
  -v /etc/machine-id:/etc/machine-id:ro \
  -v ./pacman.conf:/etc/pacman.conf:ro \
  -v /var/lib/repo/aur:/var/lib/repo/aur:O \
  --network=host \
  docker.io/archlinux/archlinux:latest \
  bash -euc 'pacman -Syu --noconfirm alpaca-ai; dbus-run-session -- alpaca'
