import unittest
import pandas.util.testing as pdt
import pandas as pd

from qiime2 import Artifact
from qiime2.plugin.testing import TestPluginBase
from qiime2.plugins import gcn_norm


class GcnNormTests(TestPluginBase):
    package = 'q2_gcn_norm.tests'

    def test_gcn_norm_silva(self):
        feature_id = ['taxon_1', 'taxon_2', 'taxon_3', 'taxon_4', 'taxon_5', 'taxon_6']
        taxa = ['D_0__Bacteria;D_1__Firmicutes;D_2__Bacilli;D_3__Lactobacillales;'\
                'D_4__Lactobacillaceae;D_5__Lactobacillus;D_6__Lactobacillus murinus',

                'D_0__Bacteria;D_1__Firmicutes;D_2__Bacilli;D_3__Lactobacillales;'\
                'D_4__Lactobacillaceae;D_5__Lactobacillus',

                'D_0__Bacteria;D_1__Bacteroidetes;D_2__Bacteroidia;D_3__Bacteroidales;'\
                'D_4__Rikenellaceae;D_5__Alistipes;D_6__Alistipes sp. N15.MGS-157',

                'D_0__Bacteria;D_1__Bacteroidetes;D_2__Bacteroidia;D_3__Bacteroidales;'\
                'D_4__Rikenellaceae;D_5__Alistipes',

                'D_0__Bacteria;D_1__Bacteroidetes;D_2__Bacteroidia;D_3__Bacteroidales',

                'Unassigned'
                ]
        confidence = [0.99]*len(feature_id)
        data_taxonomy = {'Feature ID': feature_id,'Taxon': taxa, 'Confidence': confidence}
        df_taxa = pd.DataFrame(data_taxonomy)
        df_taxa.set_index('Feature ID', inplace=True)
        taxonomy_silva = Artifact.import_data('FeatureData[Taxonomy]', df_taxa)

        df_table = pd.DataFrame([[10,10,10,10,10,10],
                                 [ 5, 5, 5, 0, 0, 0]],
                                 index=['sample A','sample B'],
                                 columns=feature_id)
        table = Artifact.import_data('FeatureTable[Frequency]', df_table)

        table_gcn_normalized = gcn_norm.actions.copy_num_normalize(table, taxonomy_silva ,database='silva')

        df_table_normalized = table_gcn_normalized.gcn_norm_table.view(pd.DataFrame)

        copy_num = [6, 5.04, 2.12, 2.12, 3.52, 1]
        df_true = df_table/copy_num

        pdt.assert_frame_equal(df_table_normalized, df_true)

    def test_gcn_norm_greengenes(self):
        feature_id = ['taxon_1', 'taxon_2', 'taxon_3', 'taxon_4', 'taxon_5', 'taxon_6']
        taxa = ['k__Bacteria; p__Firmicutes; c__Bacilli; o__Lactobacillales; '\
                'f__Lactobacillaceae; g__Lactobacillus; s__salivarius',

                'k__Bacteria; p__Firmicutes; c__Bacilli; o__Lactobacillales; '\
                'f__Lactobacillaceae; g__Lactobacillus; s__',

                'k__Bacteria; p__Firmicutes; c__Clostridia; o__Clostridiales; '\
                'f__Lachnospiraceae; g__Shuttleworthia; s__satelles',

                'k__Bacteria; p__Firmicutes; c__Clostridia; o__Clostridiales; f__; g__; s__',

                'k__Bacteria; p__Proteobacteria; c__Alphaproteobacteria; o__; f__; g__; s__',

                'Unassigned'
                ]
        confidence = [0.99]*len(feature_id)
        data_taxonomy = {'Feature ID': feature_id,'Taxon': taxa, 'Confidence': confidence}
        df_taxa = pd.DataFrame(data_taxonomy)
        df_taxa.set_index('Feature ID', inplace=True)
        taxonomy_silva = Artifact.import_data('FeatureData[Taxonomy]', df_taxa)

        df_table = pd.DataFrame([[10,10,10,10,10,10],
                                 [ 5, 5, 5, 0, 0, 0]],
                                 index=['sample A','sample B'],
                                 columns=feature_id)
        table = Artifact.import_data('FeatureTable[Frequency]', df_table)

        table_gcn_normalized = gcn_norm.actions.copy_num_normalize(table, taxonomy_silva ,database='greengenes')

        df_table_normalized = table_gcn_normalized.gcn_norm_table.view(pd.DataFrame)

        copy_num = [7, 5.04, 5.42, 4.58, 1.83, 1]
        df_true = df_table/copy_num

        pdt.assert_frame_equal(df_table_normalized, df_true)


if __name__ == '__main__':
    unittest.main()