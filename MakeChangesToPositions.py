#!/usr/bin/env python
from ROOT import TChain,TCanvas,TH1D,Double,TH2D,gROOT,gStyle,TGaxis,TRandom3
import os
import math 


class Misalignments():

	def __init__(dr):
		self.geom_file = "STM_Misalignment.txt"
		self.dx = 0.
		self.dy = 0.
		self.dz = 0.
		self.dphi = 0.
		self.dr = dr
        
	def set_new_radius(self):
		f = open(self.geom_file, 'r')
		new_radius = 5.642+self.dr
		
		for line in f:
	    		if "stm.SScollimator.hole1.radiusDnStr" in line: 
				 
				line.replace("5.642", str(new_radius))
					
		f.write()			
		f.close()
	
