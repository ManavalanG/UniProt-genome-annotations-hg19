'''
Script to parse in-house restructured UniProt genome coordinates data to keep only the data with UniProt's reviewed status.
Simple parsing and comparison is done here, instead of using pandas, numpy, etc. Hence, it takes a bit longer time (~ 1 min) to complete.

Author: 'Mana'valan Gajapathy
'''


import csv
import os
from natsort import natsorted

input_bed_file = 'hg38_uniprot_bedfiles/UP000005640_9606_beds/convert2hg19/hg19_format_fixed/merged_select_UniProt_hg19_restructured.bed'
output_filename = os.path.basename(input_bed_file).replace('.bed', '_reviewed_only.bed')


# reads file with uniprot IDs that are from human and has reviewed status
reviewed_ids = []
with open('settings_files/UniProt_IDs_human_reviewed.txt', 'Ur') as reviewed_uniprot_handle:
    for line in reviewed_uniprot_handle:
        line = line.replace('\n', '')
        reviewed_ids.append(line.lower())


# reads bedfile and writes in output if their UniProt IDs have reviewed status
match = 0
in_input = 0
reviewed_only_list = []
with open(input_bed_file, 'Ur') as input_bed_handle:
    input_bed_csv = csv.reader(input_bed_handle, delimiter='\t')
    for row in input_bed_csv:
        uniprot_id = row[3].split(':')[0].lower()
        if uniprot_id  in reviewed_ids:
            reviewed_only_list.append('\t'.join(row))
            # reviewed_only_out_handle.write('\t'.join(row) + '\n')
            # print count, uniprot_id
            match += 1
        in_input += 1

with open(output_filename, 'w') as reviewed_only_out_handle:
    title_line = ['#chrom','start_pos','end_pos','uniprot_id','seq_feature','strand','thick_start','thick_end','rgb', 'blocks','block_size','block_start','annotation_id','description']
    reviewed_only_out_handle.write('\t'.join(title_line) + '\n')
    reviewed_only_out_handle.write('\n'.join(natsorted(reviewed_only_list)))    # sorts bedfile data before writing outfile

print 'No. of annotations in input bedfile: %i\n ' \
      'Total written in to output: %i\n' \
      'Total excluded from output: %i' %(in_input, match, in_input - match)