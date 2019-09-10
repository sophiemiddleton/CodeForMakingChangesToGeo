#!/usr/bin/env python
from ROOT import TSystemDirectory, TList, TFile, TCanvas,TH1D,Double,TH2D,gROOT,gStyle,TGaxis,TRandom3
import os
import sys
import glob
import math 

def plot_particles():

	TSystemDirectory dir = "Output_Root_FoV"
	TList files = dir.GetListOfFiles()
	for i, file in enumerate(file):
		print file.GetName()


plot_particles()
	
