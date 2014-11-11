#!/usr/bin/python

import os
import zipfile

FILENAME = '.FOCA'
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

# Extract
with zipfile.ZipFile(FILENAME, READONLY) as zh:
	zh.extractall(".")

# Extract for each
for title, filename in EXTRACT_ARRAY:
	fh_output = open(title+".txt", WRITE_BINARY)
	fh_input = open(filename, READONLY)

	all_lines = fh_input.readlines()
	for line in all_lines:
		if line.find('<string>') != -1:
			fh_output.write(line[14:-11] + '\n')

	fh_output.close()
	fh_input.close()


# Cleanup
for del_file in DEL_ARRAY:
	os.system('rm ' + del_file)
