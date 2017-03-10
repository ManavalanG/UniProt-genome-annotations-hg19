UniProt provides [human genome annotation data](http://bit.ly/2mqJMjP) enabling mapping of amino acid annotations directly to reference genome coordinates, but they are available only in hg38 coordinates.  This repository converts and makes this data available in *hg19 coordinates*.

# Files for download:
Besides conversion to hg19 coordinated, few changes are made here to suit our purposes, which is to identify if query amino acids have any UniProt annotation. See *'Processing pipeline'* section for details.

* [Restructured, hg19-converted Bed files](./Download_data/hg19_UniProt_genome_annotations_Feb2017.zip). This is what you probably are interested in.
* Two merged Bed files ([type1](./Download_data/merged_select_UniProt_hg19_restructured_type1.bed) and [type0](./Download_data/merged_select_UniProt_hg19_restructured_type0.bed)) depending on the annotation type only from UniProt reviewed proteins.

* Two merged files each containing selective [sequence annotations](http://www.uniprot.org/help/sequence_annotation) of interest, as listed below, from UniProt reviewed proteins.

    a. [Merged file - Type 1](./Download_data/merged_select_UniProt_hg19_restructured_type1.bed) has following annotation types merged into a single file.

        1	Active site
        2	Binding site for any chemical group
        3	Calcium binding region
        4	Cross-link between proteins
        5	Disulfide bond
        6	Glycosylation-PTM
        7	Interesting site
        8	Lipidation-PTM
        9	Metal binding site
        10	Motif
        11	Nucleotide binding region
        12	Other PTM
        13	Signal peptide
        14	Transit peptide
        15	Zinc finger region

    b. [Merged file - Type 0](./Download_data/merged_select_UniProt_hg19_restructured_type0.bed) has following annotation types merged into a single file.

        1	Active peptide
        2	Chain
        3	Coiled coil
        4	DNA binding domain
        5	Domain
        6	Intramembrane
        7	Natural variant
        8	Region of interest
        9	Repeated motifs or domains
        10	Topological domain
        11	Transmembrane region



# Processing pipeline:

1. Use [liftOver](http://genome.ucsc.edu/cgi-bin/hgLiftOver) tool for conversion of hg38 to hg19 coordinates.
Note: If you are interested in excecuting the script, download [chain file](http://hgdownload.cse.ucsc.edu/goldenPath/hg38/liftOver/hg38ToHg19.over.chain.gz) and store it in [settings_files directory](settings_files).
It is not provided here due to license concerns.
2. Fix formatting issues in resulting Bed files.
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

[Resulting Bed files](./Download_data/hg19_UniProt_genome_annotations_Feb2017.zip) are what you probably need if you are looking for replacement for UniProt provided hg38 genome coordinates in hg19 format.


#### Further Restructuring:

We further merge sequence annotation types of our interest into two Bed files, only if such annotations have UniProt's reviewed status.

4. Filter out annotations that are not reviewed by UniProt.
5. For annotation type 'natural variant', replace disease acronyms with their complete name.
6. Merge Bed files of interest (as customized in the [settings file](./settings_files/Settings_UniProt_compare.csv); based on values 0 and 1) based on sequence annotation types into two sets of merged files.


Download the resulting merged bed files:

a. [Merged Bed file - Type 1](./Download_data/merged_select_UniProt_hg19_restructured_type1.bed)

b. [Merged Bed file - Type 0](./Download_data/merged_select_UniProt_hg19_restructured_type0.bed)


# Disclaimer
UniProt's [license](http://www.uniprot.org/help/license) applies for the genome coordinates data available in this repository.  Thanks to UniProt for permitting us to distribute this data in hg19 format.  This data is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

