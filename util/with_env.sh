#!/bin/bash

source .env
export SECRET_KEY TRELLO_API_KEY TRELLO_TOKEN MONGODB_URI
"$@"

