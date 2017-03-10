'''
Converts bed files with UniProtKB genome annotation tracks from hg-build38 to build19 using UCSC's 'liftOver' tool.
See comments in script for complications produced in liftOver's output.

Author: 'Mana'valan Gajapathy

Version changes in UniProt's format:
 1. In Feb 2017 release, amino acid details next to uniprot id in bedfiles were removed (Eg. In column 4, 'O95671:p.E44' is now just 'O95671').

'''

import os
from shutil import copyfile, copyfileobj
from glob import glob
from subprocess import call
import csv
from settings_files.fn_replace_acronyms import replace_acronyms_in_natural_variant
from pybedtools import BedTool
import shutil

# function to parse settings file
def parse_settings(settings_filename):
    settings_dict = {}
    annotations_of_interest = []
    with open(settings_filename, 'Ur') as settings_handle:
        for line in settings_handle:
            line = line.replace('\n', '')
            line_list = line.split(',')
            if line[0:2] != '##' and line.replace(',', ''):  # excldues commented and empty lines
                settings_dict[line_list[0]] = [ line_list[1], line_list[2] ]
                if line_list[2] == '1':
                    annotations_of_interest.append(line_list[0])
    return settings_dict, annotations_of_interest



# Function to fix bed file format during conversion from hg-build38 to build19.
# Also, converts rows with multiple non-continuous amino acid annotations to separate lines.
def edit_bedfile(input_bed, settings_dict, annotation_type, disulfide_bedfile, output_bed_handle):
    csv_input_bed = csv.reader(input_bed, delimiter='\t')
    for row in csv_input_bed:
        # replace score column in bed files with annotation type; score was set to zero by default by UniProt.
        if row[4] == '0':
            row[4] = settings_dict[annotation_type][0]
        else:
            print 'Error. Column# 5 (score column) must have value 0. Instead, this file has some other value. ' \
                  'Figure out why. Script terminates now.'
            raise

        # merges column 14 back together
        if len(row) > 13:
            merged_col14 = ' '.join(row[13:])
        else:
            merged_col14 = ''

        # following part is to use details of block columns in bed file to split multiple annotations into separate rows
        name = row[3].split(':')
        uniprot_id = name[0]

        # if disulfide_bedfile:         # no more needed due to format change in Feb 2017 release
            # amino_acids = ( name[1].replace('p.', '') ).split('_')
        # else:
        #     amino_acids = ( name[1].replace('p.', '') ).split(',')

        block_size_list = [ int(x) for x in row[10].split(',') ]
        block_start_list = [int(x) for x in row[11].split(',')]
        if disulfide_bedfile and merged_col14.startswith('disulfide bond_'):
            block_size_list = [3, 3]        # to account for uniprot mistakenly treating disulfide bond as continuous region

        start_site, end_site, strand = int(row[1]), int(row[2]), row[5]

        # note that in bed format, start sites are 0-based and end sites are 1-based.
        for block_no in range(0, len(block_size_list)):
            if disulfide_bedfile and merged_col14.startswith('disulfide bond_'):   # disulfide bonds forming with other polypeptide chain are ignored here and treated properly in the 'else' section
                if block_no == 0:
                    new_start = start_site
                    new_end = new_start + 3
                elif block_no == 1:
                    new_start = end_site - 3
                    new_end = new_start + 3
            else:
                new_start = start_site + block_start_list[block_no]
                new_end = new_start + block_size_list[block_no]

            # # properly connects amino acids to coordinates based on strand type
            # if strand == '+':     # no more needed due to format change in Feb 2017 release
            #     new_name = "%s:p.%s" %(uniprot_id, amino_acids[block_no])
            # else:
            #     new_name = "%s:p.%s" %(uniprot_id, amino_acids[-(block_no+1)])
            new_name = "%s" % uniprot_id

            revised_row = "%s\t%i\t%i\t%s\t%s\t%i\t%i\t%s\t1\t%i\t0\t%s\t%s\n" \
                  %(row[0], new_start, new_end, new_name, '\t'.join(row[4:6]), new_start, new_end, row[8],
                    block_size_list[block_no], row[12], merged_col14)
            output_bed_handle.write(revised_row)

    output_bed_handle.close()


# function to create directory if doesnt already exist
def mkdir_if_not_exists(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

# function to make a file and delete and make a newfile if it already exists
def create_newfile(directory, filename):
    # creates a bed file that will have merged data of bedfiles of interest
    merged_outbedfile = os.path.join(directory, filename)
    if os.path.exists(merged_outbedfile):  # deletes file if it exists. This is done to create and append to a new file.
        os.remove(merged_outbedfile)

    # Commented out since use of bedtools' sorting feature removes the title line while sorting.
    # with open(merged_outbedfile, 'w') as out_handle:    # write title
    #     out_handle.write('#chrom\tg_start\tg_end\tuniprot_id\tannotation_type\tstrand\tg_start\tg_end\trgb\tno_of_blocks\tsize_of_blocks\tstart_of_blocks\tannotation_identifier\tdescription\n')

    return merged_outbedfile


# function to append data to existing file based on annotation type
def append_to_mergefile(merged_bedfilename, fixed_bed19_outfile, settings_dict, annotation_type, annotation_value):
    with open(merged_bedfilename, 'ab') as combined_handle:
        if settings_dict[annotation_type][1] == annotation_value:
            with open(fixed_bed19_outfile, 'rb') as edited_bed:
                copyfileobj(edited_bed, combined_handle, 1024 * 1024 * 10)  # 10MB per writing chunk to avoid reading big file into memory.


# read settings file
settings_filename = 'settings_files/Settings_UniProt_compare.csv'
settings_dict, annotations_of_interest = parse_settings(settings_filename)

# get filepaths of UniProt's genome annotation track containing bed files
input_bedfiles_dir = 'hg38_uniprot_bedfiles/UP000005640_9606_beds'
input_file_list = glob(input_bedfiles_dir + '/*.bed')

build19_output_dir = os.path.join(input_bedfiles_dir, 'convert2hg19')   # dir to store liftOver output data in hg-build19 format
mkdir_if_not_exists(build19_output_dir)
fixed_bed19_outdir = os.path.join(build19_output_dir, 'hg19_format_fixed')    # dir to have format-corrected build19 bed files
mkdir_if_not_exists(fixed_bed19_outdir)

# creates a bed file that will have merged data of bedfiles with annotation types labelled as type 1 in settings file
mkdir_if_not_exists('Download_data')
merged_type1_filename = 'Download_data/merged_select_UniProt_hg19_restructured_type1.bed'
merged_bedfile_type1 = create_newfile(directory='.', filename=merged_type1_filename)

# creates a bed file that will have merged data of bedfiles with annotation types labelled as type 0 in settings file
merged_type0_filename = 'Download_data/merged_select_UniProt_hg19_restructured_type0.bed'
merged_bedfile_type0 = create_newfile(directory='.', filename=merged_type0_filename)


# liftOver tools requires chain file for propper mapping between genome assemblies
liftover_chainfile = 'settings_files/hg38ToHg19.over.chain.gz'
print "Chainfile used for liftOver: '%s\n'" % liftover_chainfile


# merged_file = 'merged_UniProt_genome_annotations_of_interest.bed'
count = 1
for bed_file in input_file_list:
    base_filename = os.path.basename(bed_file)
    build19_outfile = os.path.join(build19_output_dir, base_filename.replace('.bed', '_build19.bed'))
    error_filename = os.path.join(build19_output_dir, base_filename.replace('.bed', '_unmapped.log'))       # if coordinates could not be mapped to target assembly, this file logs them

    # uses 'liftOver' command line tool to convert coordinates to target assembly coordinates
    try:
        # if bedPlus parameter not provided, liftOver seems to convert even the columns that are not coordinates.
        # For example, when not used, it converts RGB column to new coordinates. Using this parameter converts only the columns that are within the limit provided. RGB column is column #9, btw.
        print "%i/%i - Executing liftOver for file: '%s'" % (count, len(input_file_list), bed_file)
        call(['liftOver', bed_file, liftover_chainfile, build19_outfile, error_filename, "-bedPlus=8", "-minMatch=1.0"])
    except Exception as e:
        print 'liftOver execution resulted in error:\n%s' %e
        raise
    count += 1


    # liftOver doesn't recognize bed detailed format. Though -bedplus parameter circumvents this, liftOver still has trouble dealing with space characters in column 14 of input bed file,
    # and the output bed file ends up replacing space with tab characters in that column. I haven't found any solution for this from web-search.
    # These output files, as it is, would have varying number of columns within a file, and bedtools results in error in this case.
    # Following part fixes this issue and converts them back into single column.
    # Tried using pandas and csv modules, but neither could properly handle multi-column data without complicating scripting. Hence, straight-forward scripting was done and this is lot simpler and is not taxing on time/memory either.
    fixed_bed19_outfile = os.path.join(fixed_bed19_outdir, '_'.join( ['hg19_final', base_filename]) )
    if not base_filename.endswith('_proteome.bed'):      # proteome bed file doesn't have 14-column structure as other bed files. They can be copied into a new file without any modification.
        annotation_type = base_filename.replace('UP000005640_9606_', '')
        annotation_type = annotation_type.replace('.bed', '')

        if base_filename.endswith('_disulfid.bed'):
            disulfide_bed = True
        else:
            disulfide_bed = False

        with open(fixed_bed19_outfile, 'w') as edited_bed_handle:
            # edited_bed19_data = []
            with open(build19_outfile, 'Ur') as bed19_handle:
                edit_bedfile(bed19_handle, settings_dict, annotation_type, disulfide_bed, edited_bed_handle)

        # for 'natural variant' bed file, disease acronym in column 14 need to replaced with full name
        if base_filename.endswith('_variant.bed'):
            natural_variant_bed = True
            fixed_bed19_outfile = replace_acronyms_in_natural_variant(fixed_bed19_outfile, diseases_acronym_file='settings_files/diseases-all.tab')  # replaces acronym with full name and writes them in a temporary file
        else:
            natural_variant_bed = False

            # for annotations that are labelled as type 1 in settings file
        # append into a single bed file for annotations of interest
        append_to_mergefile(merged_bedfile_type1, fixed_bed19_outfile, settings_dict, annotation_type, annotation_value='1')

        # for annotations that are labelled as type 0 in settings file
        # append into a single bed file for annotations of interest
        append_to_mergefile(merged_bedfile_type0, fixed_bed19_outfile, settings_dict, annotation_type, annotation_value='0')


        # for 'natural variant' bed file, delete the temporary bed file which had disease acronym replaced with full name
        if natural_variant_bed:
            os.remove(fixed_bed19_outfile)


    else:           # proteome bed file doesn't have 14-column structure as other bed files. They can be copied into a new file without any modification.
        copyfile(build19_outfile, fixed_bed19_outfile)


# sorts the contents of merged bed file
title_line = '#chrom\tg_start\tg_end\tuniprot_id\tannotation_type\tstrand\tg_start\tg_end\trgb\tno_of_blocks\tsize_of_blocks\tstart_of_blocks\tannotation_identifier\tdescription\n'
for filename in [merged_type0_filename, merged_type1_filename]:
    bed_data = BedTool(filename)
    bed_data.sort().saveas(filename)

    # Bedtools' sorting removes title line. Following part writes title as first line of the file
    with open(filename, 'r') as original: data = original.read()
    with open(filename, 'w') as modified: modified.write(title_line + data)


# Zips hg19 converted bed files and puts it into download directory
dir_name = os.path.join(input_bedfiles_dir, 'convert2hg19/hg19_format_fixed')
shutil.make_archive('Download_data/hg19_UniProt_genome_annotations_Feb2017', 'zip', dir_name)