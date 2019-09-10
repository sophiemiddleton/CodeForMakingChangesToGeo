#!/bin/bash
COUNTER=0
#rm -r tmp_$1 fcls$1 FCL_Outputs_Change_$1
mkdir tmp_$1 fcls_$1 FCL_Outputs_Change_$1 Output_Root_$1
while [  $COUNTER -lt 9 ]; do
             echo The counter is $COUNTER 
             
	     python main.py $COUNTER $1
             
             mv 000 FCL_Outputs_Change_$1/000_$COUNTER
             
             let COUNTER=COUNTER+1 
         done
    
