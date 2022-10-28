##script to take KEGG numbers from a file and search through another file to find matches.
##outputs a file with the KEGG number, the function, and which bins it is found in 

#to run this python script three command line arguments are needed
#first the KEGG file containing the KEGG numbers you want to search for, followed by a second column including the function/identifier of the kegg number. The columns should be tab separated. 
#second the file that you are searching through, ie your ghost koala kegg annotation file 
#third a file name you want the output to save to 

import os
import sys
import csv
import json
from sys import argv

#read in the file that contains the KEGG numbers that you want to search for using command line argument
KEGG_data_input=sys.argv[1]
KEGG_data = open(KEGG_data_input)
KEGG_lines = KEGG_data.readlines()


#create dictionary so that KEGG number and function are linked together
KEGG_dict={}

#remove newline characters, split at the tab between the KEGG number and the name of the function
#append the kegg numbers and functions to respective lists
for each in KEGG_lines:
	no_new_lines=each.rstrip()
	split_lines = no_new_lines.split("\t")
	KEGG_numbers= split_lines[0]
	KEGG_functions = split_lines[1]
	KEGG_pairs = {KEGG_numbers:[KEGG_functions]}
	KEGG_dict.update(KEGG_pairs)

#print(KEGG_dict)

#Read in the second file, this is the file that you are searching through for the kegg numbers you just put in the list (aka the metagenome data)
Metagenome_data_input = sys.argv[2]
Metagenome_data = open(Metagenome_data_input)
Metagenome_lines = Metagenome_data.readlines()

#create empty list that will hold the lines which have kegg numbers associated with the contigs 
meta_list = []

#Do the same cleaning up, remove newlines and split at tab
#remove any lines where there is no KEGG number associated with the contig by only looking at lines with a length > 1
#append the lines with kegg number associated to meta_list 
for each in Metagenome_lines:
	no_new_lines=each.rstrip()
	split_lines = no_new_lines.split("\t")
	#print(split_lines)
	if len(split_lines)>1:
		meta_list.append(split_lines)
		
#okay this will search through the meta_list for each kegg number
#and then it will append the contig name to the dictionary 
#so that now each KEGG number is a key, and the values are a list with the function followed by which contigs its found in
for KEGG in KEGG_dict:
	for each in meta_list:
		if KEGG == each[1]:
			KEGG_dict[KEGG].append(each[0])


#print(KEGG_dict)

#writes a header to the file that you will append the data to. If you don't want the header just # this out. 
with open (argv[3], 'w') as f:
	header = "KEGG" + "\t" + "Count" + "\t" + "Function" + "\t" + "Location" + "\n"
	f.write(header)

#write to the file with the headers the KEGG number, the number of times the kegg number was found, the function, and then where it was found (contigs)	
with open (argv[3], 'a') as f:	
	for key,val in KEGG_dict.items():
		string= str(key) + "\t" + str(len(val)-1) + "\t" + '\t'.join(val) + "\n"		
		f.write(string)





