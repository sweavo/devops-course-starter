#!/bin/bash
ag --ignore=expected.subcheck --vimgrep  '(KEY|TOKEN|SECRET|PAT) *=' | sort  > .subcheck.tmp
diff -C 0 .subcheck.tmp expected.subcheck 


