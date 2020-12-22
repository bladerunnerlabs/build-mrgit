#!/bin/bash

url=$1; shift
remote=$1; shift
branch=$1; shift
dir=$1; shift

if [ -d ${dir} ]; then
    git -C ${dir} fetch ${remote} 2>&1 | sed -n "s/.*/[${dir}] &/p"
    if [ -n "$(git -C ${dir} branch | grep ${branch})" ]; then
        git -C ${dir} checkout ${branch} 2>&1 | sed -n "s/.*/[${dir}] &/p"
        git -C ${dir} rebase ${remote}/${branch} 2>&1 | sed -n "s/.*/[${dir}] &/p"
    else
        git -C ${dir} checkout --track ${remote}/${branch} 2>&1 | sed -n "s/.*/[${dir}] &/p"
    fi
else # no dir
    git clone --progress --origin ${remote} --branch ${branch} ${url} ${dir} 2>&1 | sed -n "s/.*/[${dir}] &/p"
fi
