#!/bin/bash

set -eu

RESET="$(tput sgr0)"
GREEN="$(tput setaf 2)"
RED="$(tput setaf 1)"

function testone() {
	xnb="$1"
	echo -n "$xnb... "
	until ./xnbread.py "$xnb" &>/dev/null; do
		echo "${RED}Failure.${RESET}"
		./xnbread.py "$xnb" || true # run again to get the callstack/message
		echo
		read -p 'Press ENTER to retry, or Ctrl-C to give up'
	done
	echo "${GREEN}OK!${RESET}"
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
