#!/bin/bash

set -eu

RESET="$(tput sgr0)"
GREEN="$(tput setaf 2)"
RED="$(tput setaf 1)"

SCRATCH=$(mktemp)

PASSES=0
FAILS=0

declare -a FAILNAMES

function testone() {
	xnb="$1"
	out="${xnb%.xnb}.out"
	echo -n "$xnb... "
	./xnbread.py -r "$xnb" > "$SCRATCH"
	if diff -q "$out" "$SCRATCH" > /dev/null; then
		echo "${GREEN}OK!${RESET}"
		PASSES=$((PASSES+1))
	else
		echo "${RED}Failure.${RESET}"
		FAILS=$((FAILS+1))
		FAILNAMES+=("$xnb")
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
x=0
while [ $x -lt $FAILS ]; do
	echo "Failure ${x}: ${RED}${FAILNAMES[$x]}${RESET}"
	x=$((x+1))
done

echo
echo "Total: ${GREEN}${PASSES} passes, ${RED}${FAILS} failures${RESET}"

rm $SCRATCH
