#!/usr/bin/python

import os
import sys
import zipfile

READONLY = 'r'
WRITE_BINARY = 'wb'
CURRENT_DIR = '.'
TEMP_DIR = 'temp/'
EXTRACT_ARRAY = [["Emails", "metadatasummaryemails"],
				["Folders", "metadatasummaryfolders"],
				["OSs", "metadatasummaryoperatingsystems"],
				["Printers", "metadatasummaryprinters"],
				["Software", "metadatasummarysoftware"],
				["Users", "metadatasummaryusers"]]

DEL_ARRAY = ["documents","metadatasummaryemails", "metadatasummaryfolders",
				"metadatasummaryoperatingsystems", "metadatasummaryprinters",
				"metadatasummarysoftware", "metadatasummaryusers",
				"[Content_Types].xml" ]

# Damn logistics
if len(sys.argv) != 2:
	print "Need a FOCA file as an argument."
	sys.exit(1)
FILENAME = sys.argv[1]

# Extract
try:
	with zipfile.ZipFile(FILENAME, READONLY) as zh:
		zh.extractall(".")
except:
	print "Bad ZIP file.\nPet it until it's a good one."
	sys.exit(1)

# Extract for each
for title, filename in EXTRACT_ARRAY:
	fh_output = open(title+".txt", WRITE_BINARY)
	fh_input = open(filename, READONLY)

	# Check each line and write it into a file
	all_lines = fh_input.readlines()
	for line in all_lines:
		if line.find('<string>') != -1:
			fh_output.write(line[14:-11] + '\n')

	# Close the file handlers
	fh_output.close()
	fh_input.close()


# Cleanup
for del_file in DEL_ARRAY:
	os.system('rm ' + del_file)
