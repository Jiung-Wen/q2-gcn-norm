## q2-gcn-norm
QIIME 2 plugin for normalizing sequences by 16S rRNA gene copy number (GCN) based on rrnDB database

### Introduction:
This plugin normalizes sequences by 16S rRNA gene copy number (GCN) based on *rrn*DB database (version 5.6). The script matches the taxa of sequences with the ```rrnDB-5.6_pantaxa_stats_NCBI.tsv``` file, starting from the lowest rank. If a match is found, the mean of GCN for the taxon is assigned; if not, the script will try to match a higher rank until the highest rank is met. All the unassigned sequences are assumed to have one GCN.

Note that the **mean** column in the ```rrnDB-5.6_pantaxa_stats_NCBI.tsv``` is, according to the [*rrn*DB manual](https://rrndb.umms.med.umich.edu/help/), calculated from the means of the pan-taxa of immediate lower rank. Therefore, the mean of GCN might be different from the *rrn*db online search result. For example, the "mean" of GCN for bacteria is 2.02 in the downloading tsv file, whereas the mean of GCN for all the bacterial taxa is 5.0 if you search *rrn*DB online database.

### Install guide:

We assume you have a conda environment with the [QIIME 2 Core distribution](https://docs.qiime2.org/2019.10/install/) installed. First, activate the conda environment:
```
conda activate qiime2-2019.10
``` 

Next, install ```q2-gcn-norm``` with the following command:
```
conda install -c jiungwenchen q2-gcn-norm
```

### Running example:

We use artifacts from QIIME 2's "[Moving Pictures](https://docs.qiime2.org/2019.10/tutorials/moving-pictures/)" tutorial as test files. Use the following commands to download the files. 
```
# DADA2 output artifact:
wget https://docs.qiime2.org/2019.10/data/tutorials/moving-pictures/table-dada2.qza

# Taxonomic analysis output artifact:
wget https://docs.qiime2.org/2019.10/data/tutorials/moving-pictures/taxonomy.qza
```

We can normalize the FeatureTable using the command below:
```
qiime gcn-norm copy-num-normalize \
  --i-table table-dada2.qza \
  --i-taxonomy taxonomy.qza \
  --o-gcn-norm-table table-normalized.qza
```
The outputs would be an artifact  of type ```FeatureTable[Frequency] % Properties('copy_number_normalized')```.

Note that the taxonomy format should be like Greengenes' ```k__foo; p__bar; c__ ... ``` or SILVA's ```D_0__foo;D_1__bar;D_2__ ...```. Other formats are currently unsupported and will raise error.

Now you can perform analyses as you usually do in QIIME 2 with the GCN-normalized FeatureTable. For example, let's do the ANCOM analysis with the new FeatureTable and compare the result from this example with that from "Moving Pictures" tutorial.

```
# get the metadata from "Moving Pictures" tutorial
wget \
  -O "sample-metadata.tsv" \
  "https://data.qiime2.org/2019.10/tutorials/moving-pictures/sample_metadata.tsv"

# ANCOM analysis
qiime feature-table filter-samples \
  --i-table table-normalized.qza \
  --m-metadata-file sample-metadata.tsv \
  --p-where "[body-site]='gut'" \
  --o-filtered-table gut-table-normalized.qza
  
qiime taxa collapse \
  --i-table gut-table-normalized.qza \
  --i-taxonomy taxonomy.qza \
  --p-level 6 \
  --o-collapsed-table gut-table-l6-normalized.qza

qiime composition add-pseudocount \
  --i-table gut-table-l6-normalized.qza \
  --o-composition-table comp-gut-table-l6-normalized.qza

qiime composition ancom \
  --i-table comp-gut-table-l6-normalized.qza \
  --m-metadata-file sample-metadata.tsv \
  --m-metadata-column subject \
  --o-visualization l6-ancom-subject-normalized.qzv
```

**ANCOM output visualizations:**
* l6-ancom-subject.qzv (from official tutorial): [view](https://view.qiime2.org/visualization/?type=html&src=https%3A%2F%2Fdocs.qiime2.org%2F2019.10%2Fdata%2Ftutorials%2Fmoving-pictures%2Fl6-ancom-subject.qzv)  
 Screenshot:
 ![](https://imgur.com/UZwSquw.jpg)

* l6-ancom-subject_normalized.qzv (from this example): [view](https://view.qiime2.org/visualization/?type=html&src=https://rawcdn.githack.com/Jiung-Wen/miscellaneous-/9dcb49b5a701e58b3b7d5538c0eff966b75bc320/16S_copy_num_normalize/l6-ancom-subject_normalized.qzv)  
Screenshot:
![](https://imgur.com/R2y1tF5.jpg)


You may also want to compare the change in relative abundance using taxonomic bar plots:
<img src="https://imgur.com/AkTMmWn.jpg" width="600">

Generally, the GCN normalization may not have a huge impact on your analysis results, but someone (e.g. reviewer or, in my case, supervisor) may ask you to do so. For more discussion about GCN normalization, check the [related topic](https://forum.qiime2.org/t/16s-copy-number-normalization/2575) in QIIME 2 forum.
