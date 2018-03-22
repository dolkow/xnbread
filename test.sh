#!/bin/bash

set -eu

RESET="$(tput sgr0)"
GREEN="$(tput setaf 2)"
RED="$(tput setaf 1)"

SCRATCH=$(mktemp)

function testone() {
	xnb="$1"
	out="${xnb%.xnb}.out"
	echo -n "$xnb... "
	./xnbread.py -r "$xnb" > "$SCRATCH"
	if diff -q "$out" "$SCRATCH" > /dev/null; then
		echo "${GREEN}OK!${RESET}"
	else
		echo "${RED}Failure.${RESET}"
	fi
}

if [ $# -gt 0 ]; then
	while [ $# -gt 0 ]; do
		testone "$1"
		shift
	done
else
	find tests -name '*.xnb' | while read xnb; do
		testone "$xnb"
	done
fi

rm $SCRATCH
