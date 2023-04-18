SHELL=/bin/bash -u
run:
	source .env; ansible-playbook -u ec2-user -v --extra-vars "trello_api_key=$$TRELLO_API_KEY trello_token=$$TRELLO_TOKEN" playbook.yml
