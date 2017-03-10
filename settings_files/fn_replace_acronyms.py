# This script replaces disease acronym in column with full name
# Note that UniPRot's bed file has inconsistent data format in column14. UniProt clarified in private conversation that
# this file is not meant to be parsed and inconsistencies in column14 is to get around text length limit in that column.
# Same email said UniProt is planning on updating the format in April release. No specifications are known yet.

import csv
# import re


def replace_acronyms_in_natural_variant(natural_variant_file, diseases_acronym_file):
    # download diseases file from http://www.uniprot.org/diseases/
    # direct link to download - http://www.uniprot.org/diseases/?sort=&desc=&compress=yes&query=&fil=&format=tab&force=yes&columns=id
    diseases_acronym_dict = {}
    with open(diseases_acronym_file, 'Ur') as diseases_handle:
        diseases_csv = csv.DictReader(diseases_handle, delimiter = '\t')
        for row in diseases_csv:
            diseases_acronym_dict[row['Mnemonic']] = row['Name']

    out_bed_file = 'temp_NatVar_acronyms_replaced.bed'


    with open(natural_variant_file, 'Ur') as input_bed_handle, open(out_bed_file, 'w') as outbed_handle:
        input_bed_csv = csv.reader(input_bed_handle, delimiter='\t')
        for row in input_bed_csv:
            # if 'dbSNP' not in row[-1] and '(in ' in row[-1]:      # use this if varinats that are already in ClinVar needs to ignored.
            if '(in ' in row[-1]:
                col_14 = row[-1]
                col_14_list = col_14.split(' ')

                # test if each words are disease acronym, and convert them to full-names accordingly.
                # This method is not the best, but this is currently adopted since UniProt's data format in this case is not standardized completely yet.
                # Note that semicolon breaks disease terms from other type of descriptions
                # See commented out code below for more details on this data format problem.
                semicolon_check = False     # semicolon breaks disease terms from other type of descriptions
                for num in range(0, len(col_14_list)):
                    if not semicolon_check:
                        test_term = col_14_list[num]

                        # disease acronyms may end with certain symbols. They need to be removed before testing if test strings are actuallky disease acronyms
                        end_character = ''
                        end_character_list = [').', ',', ';', '.']
                        for symbol in end_character_list:
                            if test_term.endswith(symbol):
                                # print test_term
                                end_character = symbol
                                test_term = test_term.split(symbol)[0]
                                break

                        # stitch them back together
                        if test_term in diseases_acronym_dict:
                            col_14_list[num] = '"%s"%s' % (diseases_acronym_dict[test_term], end_character)

                        if end_character == ';':
                            semicolon_check = True

                row[-1] = ' '.join(col_14_list)

                # outbed_handle.write('%s\n' %('\t'.join(row)))     # use this if varinats that are already in ClinVar needs to ignored.
            outbed_handle.write('%s\n' %('\t'.join(row)))   # use this if none of the rows in input file needs to be ignored


                # # following part attempted to replace acronyms with their full-terms, but stitching the column 14 back together presented problem
                #     # back_part = col_14[col_14.index("(") + 1:col_14.rindex(")")]     # about 1.6% of rows didn't have closing parenthesis. i.e. Non-standard data format.
                #     front_part = col_14[:col_14.index("(in ")+4]
                #
                #     back_part = col_14[col_14.index("(in ")+4:]
                #     back_part_list = re.split('\.|;|\)', back_part)
                #     disease_term = back_part_list[0]
                #
                #     # if 'and' in disease_term:
                #     disease_term_list = re.split('and|,', disease_term)
                #     disease_term_list = [item.strip() for item in disease_term_list]
                #
                #     # convert acronyms to full disease names
                #     # In limited testing in case of rows with >1 diseases, acronyms, if present, were always the first term.
                #     # About 15 rows uses full-disease terms instead of acronym (for example, glioblastoma, T-cell acute lymphoblastic leukemia, etc. in feb2017 release)
                #     if disease_term_list[0] in diseases_acronym_dict:
                #         for key in range(0, len(disease_term_list)):
                #             if disease_term_list[key] in diseases_acronym_dict:     # some diseases don't have acronym. Instead, their full name is used
                #                 disease_term_list[key] = diseases_acronym_dict[disease_term_list[key]]
                #
                #
                #     # stitch them back together
                #     if len(disease_term_list) <=2:
                #         new_disease_term = ' and '.join(disease_term_list)
                #     else:
                #         new_disease_term = ', '.join(disease_term_list)
                #         new_disease_term += ' and %s' % disease_term_list[-1]
                #
                #
                #
                #
                # except ValueError:  # one row had non-standard format data without paranthesis
                #     print row[-1]
                # #     # pass

    return out_bed_file