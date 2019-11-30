from qiime2.plugin import (Plugin, Str, Choices, Properties)
from q2_types.feature_table import FeatureTable, Frequency
from q2_types.feature_data import FeatureData, Taxonomy
from q2_gcn_norm._copy_num_normalize import copy_num_normalize

plugin = Plugin(
    name='gcn-norm',
    version='2019.11',
    website='https://github.com/Jiung-Wen/q2-gcn-norm',
    package='q2_gcn_norm',
    description=('This QIIME 2 plugin normalizes sequences by 16S rRNA gene copy number (GCN)'
                 'based on rrnDB database (version 5.6). The plugin matches the taxa of sequences'
                 'with the rrnDB-5.6_pantaxa_stats_NCBI.tsv file, starting from the lowest taxonomic rank.'
                 'If a match is found, the mean of GCN for the taxon is assigned; if not, the plugin'
                 'will try to match a higher rank until the highest rank is met. All the unassigned'
                 'sequences are assumed to have one GCN.'),
    short_description='This plugin normalizes sequences by 16S rRNA gene copy number (GCN).',
)

databases = ['silva', 'greengenes']

plugin.methods.register_function(
    function=copy_num_normalize,
  
    inputs={'table': FeatureTable[Frequency],
            'taxonomy': FeatureData[Taxonomy]},
  
    parameters={'database': Str % Choices(databases)},

    outputs=[('gcn_norm_table', FeatureTable[Frequency] % Properties('copy_number_normalized'))],
  
    input_descriptions={
        'table': ('a QIIME2 artifact of type FeatureTable[Frequency]'),
        'taxonomy': ('a QIIME2 artifact of type FeatureData[Taxonomy]')
    },

    parameter_descriptions={
        'database': ('Database used for sequence taxonomic annotation.')
    },
          
    output_descriptions={
        'gcn_norm_table': ('a FeatureTable with its frequency normalized'
                           'by each taxon\'s 16S gene copy number')
    },
  
    name='16S gene copy number normalization',
  
    description=('Normalizes sequences by their 16S rRNA gene copy number.')
)
