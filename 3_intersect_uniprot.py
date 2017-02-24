'''
This is test script on finding UniProt annotations that intersect query annotations.
It's still in primal stage.

Author: 'Mana'valan Gajapathy

'''



from pybedtools import BedTool
import StringIO

# query_regions = ['chr1:1192505', 'chr1:1244526-1244528', 'chr1:32098108-32098121']
# query_regions = ['chr1:1192505', 'chr1:1244526-1244528']
query_regions = ['chr16:74700742-74700743']
# query_regions = ['chr1:2498751']

# read input query and convert to bed file 3-column format
b_bed = ''
for query in query_regions:
    query = query.replace(',', '')
    query_list = query.split(':')
    chrm = query_list[0]
    if '-' in query_list[1]:    # includes only one nucleotide
        query_region = query_list[1].split('-')
        start = int(query_region[0]) - 1        # start is 0-based
        end = query_region[1]                   # end is 1-based
    else:                       # includes more than only one nucleotide
        start = int(query_list[1]) - 1
        end = start + 1

    b_bed += '%s\t%i\t%s\n' % (chrm, start, str(end))
# print b_bed


# intersect to UniProt's genome annotation bed files (only of those interest to us as noted in settings file)
uniprot_bed_file = 'merged_select_UniProt_hg19_restructured_reviewed_only.bed'
a = BedTool(uniprot_bed_file)
intersection = a.intersect(StringIO.StringIO(b_bed), wo= True)
if intersection:
    print intersection
    intersection.saveas('output_intersecting.bed')
else:
    print 'No intersections found.'