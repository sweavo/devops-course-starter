#!/bin/bash
set -e
set -u

TMP=$(mktemp .tmp_test_dockerignore_XXXXXX)
echo $TMP
function tidy {
    rm -v $TMP
}
trap tidy EXIT


fail_flag=false
pass_flag=false

function fail {
    echo "FAIL: $@"
    fail_flag=true
}

function pass {
    echo "Pass: $@"
    pass_flag=true
}


echo "PREPARE"
echo "======="

( 
    set -x 
    make image
    make run-docker DOCKER_TAIL="find ." | tail +3 | tee "$TMP" 
)

echo "CHECKS"
echo "======"

set -x

if grep '.env' "$TMP" 
then fail "contained a file called .env, or close enough to be worried"
else pass
fi

if grep '^\./\.' "$TMP" 
then fail "contained a dotfile"
else pass
fi 

if grep '__pycache__' "$TMP" 
then fail "contained a __pycache__"
else pass
fi

if grep '^./todo_app/__init__.py$' "$TMP"
then pass 
else fail "Missing __init__.py"
fi

if grep '^./poetry.lock' "$TMP" 
then pass
else fail "Missing poetry.lock"
fi

if grep '^./pyproject.toml' "$TMP" 
then pass
else fail "Missing pyproject.toml"
fi
set +x


echo "DONE"
echo "===="

echo -n "Summary: "
if $pass_flag
then if $fail_flag
    then echo "FAIL. There were failures"
    else echo "PASS"
    fi
else if $fail_flag
    then echo "FAIL. Everything went wrong"
    else echo "FAIL. No tests?"
    fi
fi
