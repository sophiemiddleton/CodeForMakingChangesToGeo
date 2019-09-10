#!/usr/bin/env python
import ROOT
from ROOT import TChain,TCanvas,TH1D,Double,TH2D,gROOT,gStyle,TGaxis,TRandom3
import os
import sys
import glob
import math 
import subprocess
import shutil
geom_file = "STM_Original.txt"

SS_design_radius = 5.642
FoV_design_radius = 71.0
base_dir = os.path.join("/mu2e/app/users/sophie/STM_study/fcl/Analysis")

##### First Section: Getting FCLS & Multiple ROOT Output FIles ############
def dir_name():
	target_name = "Output_Logs"
	return target_name

def substitute(file_name_in, file_name_out, switch_dict):
  """
  Read in file_name_in and write to file_name_out, replacing key with value in switch_dict. Must be a built in function somewhere to do same...

  - file_name_in  = string name of the input file
  - file_name_out = string name of the output file
  - switch_dict   = dict of values to be swapped to the values they will be swapped for

  e.g. common.substitute('file.in', 'file.out', {'energy':'momentum'})
  """
  fin  = open(file_name_in,  'r')
  fout = open(file_name_out, 'w')
  for line in fin:
    for key, value in switch_dict.iteritems():
      line = line.replace(str(key), str(value))
    fout.write(line)
  fin.close()
  fout.close()

def set_new_SS_position(i,new_position):
	"""
	Simple function to chnage the position of the SS in x,y,z
	"""
	f = open(geom_file, 'r+')
	t= open("tmp_SS/tmp"+str(i)+".txt",'w')
	for line in f:

    		if "stm.SScollimator.hole1.radiusDnStr" or "double stm.SScollimator.hole2.radiusDnStr" in line: 
			t.write( line.replace( "5.642", str(new_radius) ) )
		else:
			t.write(line)  
	make_fcl(i,"SS", new_radius)     
	t.close()	
	f.close()

def set_new_SS_radius(i,new_radius):
	"""
	Simple function to switch radius to new value and save in .txt. file

	"""
	f = open(geom_file, 'r+')
	t= open("tmp_SS/tmp"+str(i)+".txt",'w')
	for line in f:

    		if "stm.SScollimator.hole1.radiusDnStr" or "double stm.SScollimator.hole2.radiusDnStr" in line: 
			t.write( line.replace( "5.642", str(new_radius) ) )
		else:
			t.write(line)  
	make_fcl(i,"SS", new_radius)     
	t.close()	
	f.close()

def set_new_FoV_radius(i,new_radius):
	"""
	Simple function to switch radius to new value and save in .txt. file
	"""
	f = open(geom_file, 'r+')
	t= open("tmp_FoV/tmp"+str(i)+".txt",'w')
	for line in f:

    		if "stm.FOVcollimator.hole1.radiusDnStr " or "stm.FOVcollimator.hole2.radiusDnStr" in line: 
			t.write( line.replace( "71.0", str(new_radius) ) )
		else:
			t.write(line)  
	make_fcl(i,"FoV", new_radius)     
	t.close()	
	f.close()

def make_fcl(i,element,new_radius):
	"""
	Simple function to switch radius to new value and save in .fcl. file
	"""
	f = open("/mu2e/app/users/sophie/STM_study/fcl/Analysis/fcls_"+str(element)+"/radius.fcl", 'r+')
	t= open("fcls_"+str(element)+"/tmp"+str(i)+".fcl",'w')
	for line in f:
    		if "GeometryService" in line: 
			t.write( line.replace( "Mu2eG4/geom/STM_Misalignment.txt", "Mu2eG4/geom/tmp"+str(i)+".txt" ) )
                #/mu2e/app/users/sophie/STM_study/fcl/Analysis/tmp_"+str(element)+	
		else:
			t.write(line)       
	t.close()	
	f.close()

def loop(a, val, element):
	"""
	loops through and makes incremented chnages to radius. Each is saved as separate file
	"""
	for i in range(0,a):
		new_radius=val+(i/100.)
		if element == "SS":
    			set_new_SS_radius(i,new_radius)
		if element == "FoV":
    			set_new_FoV_radius(i,new_radius)
		else:
			return

def get_file_list():#TODO
   """
   retreives list of geometry files
   """
   os.path.join("/mu2e/app/users/sophie/STM_study/fcl/fcls")
   file_list = []
   return file_list


def move_file(i, input_file, output_file):
    """
    moves 000 to new directory
    """
    print "moving ", input_file, " to ", output_file
    #geo_path_in = os.path.join("/mu2e/app/users/sophie/STM_study/fcl/Analysis")
    out_dir = dir_name()
    log_name = out_dir+'/move'+str(i)+'.log'  
    move = ["mv",input_file, output_file]
    log_file = open(log_name, 'w')
    subproc = subprocess.Popen(move, stdout=log_file, stderr=subprocess.STDOUT)
    return subproc

def generate_fcls(i,element):
    """
    generates fcl and saves outputs....
    """
    out_dir = dir_name()
    log_name = out_dir+"/generation"+str(i)+".log"
    #geo_path_in = os.path.join("/mu2e/app/users/sophie/STM_study/fcl/Analysis/fcls/tmp"+str(i)+".fcl")
    re_generate = ["generate_fcl", "--description=STM_sophie_1", "--dsconf=v1",  "--merge-factor=10",  "--inputs","/mu2e/app/users/sophie/STM_study/fcl/yaquins_inpits.list","--embed", "/mu2e/app/users/sophie/STM_study/fcl/Analysis/fcls_FoV/tmp"+str(i)+".fcl"] 
    log_file = open(log_name, 'w')
    subproc = subprocess.Popen(re_generate, stdout=log_file,  stderr=subprocess.STDOUT)
    print i, " generating fcls from ", "/mu2e/app/users/sophie/STM_study/fcl/Analysis/fcls"+str(element)+"/tmp"+str(i)+".fcl"
    
    return subproc


    

def run_file(i,element):
    """
    Runs simulation
    """
    #"-T", "/mu2e/app/users/sophie/STM_study/fcl/Analysis/Output_Root_"+str(element)+"/"+str(i)+".root"
    out_dir = dir_name()
    log_name = out_dir+'/simulation.log'
    run = ["mu2e", "-c", "/mu2e/app/users/sophie/STM_study/fcl/Analysis/FCL_Outputs_Change_"+str(element)+"/000_"+str(i)+"/cnf.sophie.STM_sophie_1.v1.001002_00000600.fcl", "-S", "/mu2e/app/users/sophie/STM_study/fcl/yaquins_inpits.list","--config-out", "Output_Root_"+str(element)+"/"+str(i)+".root", "-n", "100"]
    log_file = open(log_name, 'w')
    print "ran " ,"/mu2e/app/users/sophie/STM_study/fcl/Analysis/FCL_Outputs_Change_"+str(element)+"/000_"+str(i)+"/cnf.sophie.STM_sophie_1.v1.001002_000*.fcl", " Output Saved as: ","/mu2e/app/users/sophie/STM_study/fcl/Analysis/Output_Root_"+str(element)+"/"+str(i)+".root"
    subproc = subprocess.Popen(run)
    return subproc

def copy_geom(a,b):
    """
    Move .txt file to the geom directory
    """
    out_dir = dir_name()
    log_name = out_dir+'/copy.log'
    run = ["cp","tmp_"+str(b)+"/tmp"+str(a)+".txt", "/mu2e/app/users/sophie/Offline/Mu2eG4/geom"]
    log_file = open(log_name, 'w')
    print "cp","tmp_"+str(b)+"/tmp"+str(a)+".txt", "/mu2e/app/users/sophie/Offline/Mu2eG4/geom"
    subproc = subprocess.Popen(run, stdout=log_file, stderr=subprocess.STDOUT)
    return subproc

def rm_geom(a,b):
    """
    Remove .txt file to the geom directory
    """
    out_dir = dir_name()
    log_name = out_dir+'/removal.log'
    run = ["rm", "-r", "/mu2e/app/users/sophie/Offline/Mu2eG4/geom/tmp"+str(a)+".txt"]
    log_file = open(log_name, 'w')
    print "rm", "/mu2e/app/users/sophie/Offline/Mu2eG4/geom/tmp"+str(a)+".txt"
    subproc = subprocess.Popen(run)
    return subproc

######## Section 2: Analysing the ROOT Files ######
def get_root_files(b):
    """
    Get output file list
    """
    os.chdir("Output_Root_"+str(b))
    files = []
    for file in glob.glob("*.root"):
    	files.append(file)
    return files

pid= []

#dimensions of colls
radius_FoV = 70.0
centre_FoV_x = -3904.0
x_offset_SS = 40.6
radii_SS = 5.62



def plot(a,b, file_name):
    """
    Open root file, find branches, do analysis
    """
    print file_name
    #init of counters:
    photons = 0
    electrons=0	
    muons=0
    neutrons = 0
    tree = ROOT.TTree( 'tree', 'tree' )
    tree = file_name.Get("readsd/ntsdext")
    Nevts = tree.GetEntries()

    VID_List = [81,86,87,88,89,90,100,101,111]


    for event in range(1, Nevts):
	tree.GetEntry(event);
        
	#for vid in range (0,len(VID_List)):
	if(tree.sdid == 100):
                        
		if(abs(tree.pdg) ==2112):
		    neutrons+=1
		if(abs(tree.pdg) ==11):
		    electrons+=1
		if(abs(tree.pdg) ==13):
		    muons+=1
		if(abs(tree.pdg) ==22):
		    photons+=1
		
			
    print photons,electrons,neutrons, muons	
				


def main(a,b):
        """
	loop(int(a), FoV_design_radius, b)  
        copy_geom(a,b)
	generate_fcls(a,b)
        #run_file(a, b)  
	"""
	file_name =  ROOT.TFile("Output_Root_"+str(b)+"/"+str(b)+str(a)+".root")
	plot(a,b,file_name) 

if __name__ == "__main__":
    print sys.argv
    main(sys.argv[1], sys.argv[2])
    print "Finished"
