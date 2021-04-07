from setuptools import setup, find_packages

setup(
    name="q2-gcn-norm",
    version="2021.04",
    packages=find_packages(),
    author="Jiung-Wen Chen",
    author_email="jiung-wen.chen@wustl.edu",
    description="Normalizes sequences by their 16S rRNA gene copy number.",
    license="BSD-3-Clause",
    url="https://qiime2.org",
    entry_points={
        'qiime2.plugins':['q2-gcn-norm=q2_gcn_norm.plugin_setup:plugin']
    },
    package_data={'q2_gcn_norm': [
        'rrnDB-5.7_pantaxa_stats_NCBI.tsv',
        'tests/*',
        'citations.bib'
    ]},
    zip_safe=False,

)
