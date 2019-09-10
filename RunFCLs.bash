#!/bin/bash
COUNTER=0
#rm -r tmp_$1 fcls$1 FCL_Outputs_Change_$1
mkdir tmp_$1 fcls_$1 FCL_Outputs_Change_$1 Output_Root_$1
while [  $COUNTER -lt 9 ]; do
             echo The counter is $COUNTER 
             
	     mu2e -c "/mu2e/app/users/sophie/STM_study/fcl/Analysis/FCL_Outputs_Change_"$1"/000_"$COUNTER"/cnf.sophie.STM_sophie_1.v1.001002_00000600.fcl" -S "/mu2e/app/users/sophie/STM_study/fcl/yaquins_inpits.list" --config-out "Output_Root_"$1/$COUNTER".root" -n 100
             mv "nts.MU2EGRIDDSOWNER.cd3-beam-g4s2ToSTM.MU2EGRIDDSCONF.001002_00000600.root" "Output_Root_"$1"/"$1$COUNTER".root"
             let COUNTER=COUNTER+1 
         done

