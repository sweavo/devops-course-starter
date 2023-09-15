set -x
docker container ps --all| fgrep todo | awk '{print $1}' | xargs -r docker container remove
docker image ls| fgrep todo | awk '{print $3}' | xargs -r docker image rm
docker container ps --all| fgrep devops-course-starter | awk '{print $1}' | xargs -r docker container remove
docker image ls| fgrep devops-course-starter | awk '{print $3}' | xargs -r docker image rm
