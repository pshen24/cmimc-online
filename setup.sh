#!/bin/sh

set -eux

if [ ! -d "./website/problem_graders" ]
then
	cp -nr ./website/example_problem_graders ./website/problem_graders
fi

docker-compose up --build
