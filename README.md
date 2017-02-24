UniProt provides [human genome annotation data](ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/genome_annotation_tracks/) enabling mapping of amino acid coordinates directly to reference genome coordinates,
but only available as hg38 coordinates.  This repository converts and makes this data available in hg19 coordinates.


# Processing pipeline:

1. Uses [liftOver](http://genome.ucsc.edu/cgi-bin/hgLiftOver) tool for conversion of hg38 to hg19 coordinates.
Note: If you are interested in excecuting the script, download this chain file (TODO: add link) and store it in settings_files directory (TODO: add link).
It is not provided here due to license concerns.
2. Fix formatting issues in resulting bed files
3. Reformat bedfiles as follows:

    a. Replace score column (5th column), which is zero by default in UniProt provided data, with corresponding [sequence annotation type](http://www.uniprot.org/help/sequence_annotation) as shown below.

    ```
    Original format by UniProt:
    >chr1	7970956	7970959	Q99497	0	+	7970956	7970959	255,102,102	1	3	0	.	Nucleophile. Pubmed:20304780, Pubmed:25416785

    Format used here after conversion:
    >chr1	8031016	8031019	Q99497	Active site	+	8031016	8031019	255,102,102	1	3	0	.	Nucleophile. Pubmed:20304780, Pubmed:25416785
    ```


    b. Restructure rows in bedfiles that have >1 non-continuous amino acids as in example below.

    ```
    Original format by UniProt (this line has coordinates for three, non-continuous amino acids):
    >chr1	1633782	1633815	O75900	0	+	1633782	1633815	0,153,0	3	3,3,3	0,12,30	.	Zinc; catalytic.

    Format used here after conversion (one amino acid per row, if non-continuous):
    >chr1	1569161	1569164	O75900	Metal binding site	+	1569161	1569164	0,153,0	1	3	0	.	Zinc; catalytic.
    >chr1	1569173	1569176	O75900	Metal binding site	+	1569173	1569176	0,153,0	1	3	0	.	Zinc; catalytic.
    >chr1	1569191	1569194	O75900	Metal binding site	+	1569191	1569194	0,153,0	1	3	0	.	Zinc; catalytic.
    ```

Resulting data (TODO: Insert hg19 zip file link) is what you probably need if you are looking for replacement for UniProt provided hg38 genome coordinates in hg19 format.


## Further Restructuring:
We further merge sequence annotation types of our interest into a single bed file, only if such annotations have reviewed status from UniProt.
4. Merge bedfiles of interest (as cutomized in setting file (TODO: insert setting file link)) based on sequence annotation types into a single file (TODO: insert link).
5. Filter out the annotations that are not reviewed by UniProt.


# Disclaimer
UniProt's [license](http://www.uniprot.org/help/license) applies for the data available here.  We would like to thank UniProt for providing us permission to redistribute this data in hg19 assembly format.

