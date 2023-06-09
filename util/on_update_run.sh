#!/bin/env bash

TMP=$(mktemp .on_upXXXXX)
function tidy {
	rm "$TMP"
}
trap tidy EXIT

command="$1"
shift

while true
do
	sleep 2
	dirty=false
	for file in "$@"
	do
		if [[ "$file" -nt "$TMP" ]]
		then
			dirty=true
		fi
	done
	if $dirty
	then
		$command
		touch $TMP
	fi
done


