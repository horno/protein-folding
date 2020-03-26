#!/bin/bash


date=`date +'[%d-%m-%Y][%H:%M:%S]:'`
time="$(time ( ./folder.py -bn ) 2>&1 1>/dev/null )"

echo $date$time  | tee -a benchs.dat

