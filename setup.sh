#!/bin/bash

function setup () {
    echo $1 > darknet_path.txt
}

if [ $1 = '-h' ]
then
    echo usage: setup.sh [Darknet Path]
else
    setup $1
fi