#!/bin/bash

TMP=$(mktemp .touch.XXXX)
function tidyup {
	rm $TMP
}
trap tidyup EXIT

WATCH="$1"
shift

touch -t010101010101 "$TMP"

while true
do
	sleep 1
	if [[ "$WATCH" -nt "$TMP" ]]; then
		touch $TMP
		clear
		echo -n '==> '"$*"'  '
		date +%T
		"$@"
		echo '<== '$?
	fi
done

