#!/bin/bash

# Barebones test infrastructure check function: execute a bash command, print whether or not it returned
# zero status code, and set a flag if not.
function check {
	
	"$@"
	result=$?
	if [[ '0' == "$result" ]]
	then
		echo 'Pass'
	else
		echo 'FAIL'
		fail_flag=true
	fi	
}

fail_flag=false

# global setup
rm -rf t
mkdir t

# Gonna need an instance to test; grab its PID for killing at the end
poetry run flask run & to_kill=$!; sleep 10

# test 1
## setup 
rm -f t/t1.actual
echo -n "Hello World!" > t/t1.expected
## Execute
curl -o t/t1.actual http://localhost:5000/test
## Check
check diff t/t1.expected t/t1.actual


# Summary
echo -n "Overall result: "
if $fail_flag; then
	echo "FAILURES"
else
	echo "Passed"
fi

# Cleanup. Leave the t folder around for the user to inspect at leisure
kill $to_kill

