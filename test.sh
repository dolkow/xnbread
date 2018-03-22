#!/bin/bash

set -eu

RESET="$(tput sgr0)"
GREEN="$(tput setaf 2)"
RED="$(tput setaf 1)"

SCRATCH=$(mktemp)

for xnb in tests/*.xnb; do
	out="${xnb%.xnb}.out"
	echo -n "$xnb... "
	./xnbread.py -r "$xnb" > "$SCRATCH"
	if diff -q "$out" "$SCRATCH" > /dev/null; then
		echo "${GREEN}OK!${RESET}"
	else
		echo "${RED}Failure.${RESET}"
	fi
done
rm $SCRATCH
