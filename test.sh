#!/bin/bash

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

poetry run flask run & to_kill=$!; sleep 1

# t1
# setup 
rm -f t/t1.actual
echo -n "Hello World!" > t/t1.expected
# Execute
curl -o t/t1.actual http://localhost:5000/
# Check
check diff t/t1.expected t/t1.actual



echo -n "Overall result: "
if $fail_flag; then
	echo "FAILURES"
else
	echo "Passed"
fi

kill $to_kill

