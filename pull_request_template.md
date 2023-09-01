# Project exercise submission for module __

## M1

- [ ] Anyone could run the app following the README instructions
- [ ] You can create a new to-do item and see it immediately appear on the page
- [ ] You’re raising the Pull Request against your own repository (e.g. github.com/YourUserNameHere/My-Project-Name, not github.com/CorndelWithSoftwire/DevOps-Course-Starter)
- [ ] Your repository is public, or you’ve added all the tutors as Contributors (see the end of Setup Step 1)

## M2

- [ ] Your Trello API key and token aren’t committed in git
- [ ] You can run your app, add an item, then change its status, and those changes are persisted (on your Trello board)
- [ ] Your README includes any new steps required to set up your app and any new environment variables have placeholders in your .env.template file
- [ ] Your new Item class is used by the code that displays your index page
- [ ] You’ve deleted any unused or commented out code - it’ll be in your git history if you need it

## M3

- [ ] You have at least one unit test and at least one integration test and the tests are true to their archetype
- [ ] The unit tests each test one file/class and nothing else, without depending on their environment
- [ ] The integration tests use mocking to avoid making external requests, and don’t have access to real credentials
- [ ] If you have an e2e test, the e2e test loads real credentials and performs some browser interaction resulting in requests to Trello
- [ ] All your tests test something meaningful - they should probably all contain at least one assert
- [ ] Your README documents any set up steps required, as well as how to run your tests
- [ ] When running poetry run pytest or poetry run pytest path/to/test_file from a terminal (outside of any IDE) your tests run and pass
- [ ] Your submission still satisfies the criteria from all previous exercises

## M4

- [ ] Your playbook is able to run your to-do app on a host without you manually SSHing to the host at any point.
- [ ] Your README documents the command to provision a VM from an Ansible Control Node
- [ ] You have committed relevant files to Git and pushed them to your repository:
- [ ] Inventory file
- [ ] Playbook file
- [ ] .env.j2
- [ ] todoapp.service
- [ ] No sensitive values are contained in those files. Sensitive values should instead be passed to Ansible when you run the playbook.
- [ ] Your submission still satisfies the criteria from all previous exercises

## M5

- [ ] A single, multi-stage Dockerfile is used to specify development and production containers
- [ ] Your production container uses a production-ready server (gunicorn) to run the app
- [ ] Your readme contains instructions on how to build and run development and production containers
- [ ] Including how to mount your project in the development container so that flask automatically reloads when you edit your Python files
- [ ] No secrets are included in the built images
- [ ] Your submission still satisfies the criteria from previous exercises - it should still run outside of Docker!

## M6

(C4 exercise)

## M7

- [ ] Can I run the docker tests from instructions in the README?
- [ ] Does the pipeline run on push and on pull request
- [ ] Does the pipeline run all the tests
- [ ] There are no secret values introduced in the pushed commits
