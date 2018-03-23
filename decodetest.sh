#!/bin/bash

set -eu

RESET="$(tput sgr0)"
GREEN="$(tput setaf 2)"
RED="$(tput setaf 1)"

function testone() {
	xnb="$1"
	echo -n "$xnb... "
	if ./xnbread.py "$xnb" &>/dev/null; then
		echo "${GREEN}OK!${RESET}"
	else
		echo "${RED}Failure.${RESET}"
		echo
		./xnbread.py "$xnb" || true # run again to get the callstack/message
		exit 1
	fi
}

if [ $# -gt 0 ]; then
	while [ $# -gt 0 ]; do
		testone "$1"
		shift
	done
else
	readarray -t xnbfiles < <(find tests -name '*.xnb')
	for xnb in "${xnbfiles[@]}"; do
		testone "$xnb"
	done
fi

echo
echo "${GREEN}All files parsed without crashes${RESET}"

rm $SCRATCH
