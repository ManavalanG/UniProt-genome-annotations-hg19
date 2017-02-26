UniProt provides [human genome annotation data](http://bit.ly/2mqJMjP) enabling mapping of amino acid annotations directly to reference genome coordinates, but they are available in hg38 coordinates.  This repository converts and makes this data available in *hg19 coordinates*.

# Files for download:
Besides conversion to hg19 coordinated, few changes are made here to suit our purposes. See *'Processing pipeline'* section for details.

* [Restructured and hg19-converted Bed files](hg19_UniProt_genome_annotations.zip). This is what you probably are interested in.
* [Merged bedfile](merged_select_UniProt_hg19_restructured.bed) containing only selected 17 [sequence annotations](http://www.uniprot.org/help/sequence_annotation) of interest, as listed below, from UniProt reviewed proteins.

        1. Active site
        2. Binding site for any chemical group
        3. Calcium binding region
        4. Glycosylation-PTM
        5. Cross-link between proteins
        6. Disulfide bond
        7. Lipidation-PTM
        8. Metal binding site
        9. Other PTM
        10. Motif
        11. Nucleotide binding region
        12. Region of interest
        13. Signal peptide
        14. Interesting site
        15. Transit peptide
        16. Natural variant
        17. Zinc finger region



# Processing pipeline:

1. Uses [liftOver](http://genome.ucsc.edu/cgi-bin/hgLiftOver) tool for conversion of hg38 to hg19 coordinates.
Note: If you are interested in excecuting the script, download [chain file](http://hgdownload.cse.ucsc.edu/goldenPath/hg38/liftOver/hg38ToHg19.over.chain.gz) and store it in [settings_files directory](settings_files).
It is not provided here due to license concerns.
2. Fix formatting issues in resulting Bed files
3. Reformat Bed files as follows:

    a. Replace score column (5th column), which is zero by default in UniProt provided data, with corresponding [sequence annotation type](http://www.uniprot.org/help/sequence_annotation) as shown below.

    ```
    Original format by UniProt:
    >chr1	7970956	7970959	Q99497	0	+	7970956	7970959	255,102,102	1	3	0	.	Nucleophile. Pubmed:20304780, Pubmed:25416785

    Format we used here:
    >chr1	8031016	8031019	Q99497	Active site	+	8031016	8031019	255,102,102	1	3	0	.	Nucleophile. Pubmed:20304780, Pubmed:25416785
    ```


    b. Restructure the rows in Bed files that have non-continuous amino acids as in example below.

    ```
    Original format by UniProt (this line has coordinates for three, non-continuous amino acids):
    >chr1	1633782	1633815	O75900	0	+	1633782	1633815	0,153,0	3	3,3,3	0,12,30	.	Zinc; catalytic.

    Format we used here (one amino acid per row, if non-continuous):
    >chr1	1569161	1569164	O75900	Metal binding site	+	1569161	1569164	0,153,0	1	3	0	.	Zinc; catalytic.
    >chr1	1569173	1569176	O75900	Metal binding site	+	1569173	1569176	0,153,0	1	3	0	.	Zinc; catalytic.
    >chr1	1569191	1569194	O75900	Metal binding site	+	1569191	1569194	0,153,0	1	3	0	.	Zinc; catalytic.
    ```

    [Resulting Bed files](hg19_UniProt_genome_annotations.zip) are what you probably need if you are looking for replacement for UniProt provided hg38 genome coordinates in hg19 format.



**Further Restructuring:**

We further merge sequence annotation types of our interest into a single Bed file, only if such annotations have reviewed status from UniProt.

4. Merge Bed files of interest (as cutomized in [setting file](./settings_files/Settings_UniProt_compare.csv) based on sequence annotation types into a single file.
5. Filter out the annotations that are not reviewed by UniProt.

Download the resulting [merged Bed file here](merged_select_UniProt_hg19_restructured.bed).


# Disclaimer
UniProt's [license](http://www.uniprot.org/help/license) applies for the genome coordinates data available in this repository.  Thanks to UniProt for permitting us to distribute this data in hg19 format.  This data is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

