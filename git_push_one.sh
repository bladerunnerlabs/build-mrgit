#!/bin/bash

url=$1; shift
remote=$1; shift
branch=$1; shift
dir=$1; shift

if [ -d ${dir} ]; then
    if [ -n "$(git -C ${dir} branch | grep ${branch})" ]; then
        git -C ${dir} checkout ${branch} 2>&1 | sed -n "s/.*/[${dir}] &/p"
        git -C ${dir} push ${remote} ${branch} 2>&1 | sed -n "s/.*/[${dir}] &/p"
    else
        echo "${dir} has no branch ${branch}, can't push"
        exit 1
    fi
else # no dir
    echo "module directory ${dir} not found, can't push"
    exit 1
fi
