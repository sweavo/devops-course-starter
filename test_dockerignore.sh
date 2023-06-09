#!/bin/bash

TMP=$(mktemp .tmp_test_dockerignore_XXXXXX)
echo $TMP
function tidy {
    rm -v $TMP
}
trap tidy EXIT
