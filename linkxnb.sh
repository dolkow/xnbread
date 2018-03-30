#!/bin/bash

if [ -e "$(pwd)/$(basename $0)" ]; then
	echo "you probably want to go into another directory to do this."
	exit 1
fi

ROOT="$(readlink -e """$1""")"

find "$ROOT" -type d | while read SRC; do
	DST="$(readlink -m ."${SRC#$ROOT}")"
	if readlink -e "$SRC"/*.xnb > /dev/null; then
		mkdir -p "$DST"
		ln -s "$SRC"/*.xnb "$DST" > /dev/null
	fi
done
