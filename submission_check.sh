#!/bin/bash
git ls-files| fgrep -v expected.subcheck | xargs egrep '(KEY|TOKEN|SECRET|PAT|URI) *=' | sort  > .subcheck.tmp
diff -C 0 .subcheck.tmp expected.subcheck 
