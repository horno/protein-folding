#!/bin/bash

# To add a test, comment the protein desired to be tested like below
# and run the script with the parammeter -r one time, like ./test.sh -r

#HPH
#PPHPHHP
#HHHHPPPPP
#HPHHPHHPPHHH
#HHPHPPHPHHHPHPHH
#HPPHPPHPHPPHPPHPHP
#HPHHHHHPHHHHHHPHPH -n -f=20000
#HHHHH
#PPPPP

generate_output () {
    ./folder.py -p=$2 > outputs/correct$1.out
    echo "Test $1 generated"
}

test_output () {
    test_number=$1
    protein_to_test=$2
    diff <(cat outputs/correct$test_number.out) <(./folder.py -p=$protein_to_test) &&\
        echo "Test $test_number passed successfully"                       ||\
        echo "Test $test_number failed"                 
}

[ "$1" == "-r" ] && rm outputs/*

counter=0
while read -r name value
do
    if [ "${name:0:2}" == "#P" ] || [ "${name:0:2}" == "#H" ]
    then
        counter=$(( $counter+1 ))
        if [ "$1" == "-r" ]
        then
            generate_output $counter ${name:1}
        else 
            test_output $counter ${name:1}
        fi
    fi
done < test.sh

