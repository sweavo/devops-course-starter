#!/bin/bash

make run-dev &

server_pid=$!

function tidyup() {
    echo >&2 "Kill server ($server_pid)"
    kill $server_pid
}
trap tidyup EXIT


echo >&2 "Wait for server"

timeout=30 
url="http://127.0.0.1:5000"  

until curl --output /dev/null --silent --head --fail $url; do
    sleep 1
    ((timeout--))
    if [ $timeout -eq 0 ]; then
        echo >&2 "Timeout waiting for Flask server to start."
        exit 1
    fi
done

echo >&2 "Server is up. running '$@'"
"$@"

