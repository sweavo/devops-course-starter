#!/bin/bash

source .env
export SECRET_KEY MONGODB_URI
"$@"

