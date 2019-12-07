import os
import re
import pandas as pd


def copy_num_normalize(table: pd.DataFrame,
                       taxonomy: pd.DataFrame) -> pd.DataFrame:

    dir_path = os.path.dirname(os.path.abspath(__file__))

    df_rrndb = pd.read_csv(dir_path+'/rrnDB-5.6_pantaxa_stats_NCBI.tsv', sep='\t')

    taxon2copynum = dict(zip(df_rrndb['name'],df_rrndb['mean']))

    d = {'taxon': taxonomy['Taxon'], 'copy_number': [1]*len(taxonomy['Taxon'])}
    df_copy_num = pd.DataFrame(d)
    
    # Check taxonomy format
    for index, taxon in enumerate(taxonomy['Taxon']):
        if 'D_0__' in taxon:
            database = 'silva'
            ranks = ['D_6__', 'D_5__', 'D_4__', 'D_3__', 'D_2__', 'D_1__', 'D_0__']
            break

        elif '; p__' in taxon:
            database = 'greengenes'
            ranks = ['; s__', '; g__', '; f__', '; o__', '; c__', '; p__', 'k__']
            break
            
        else:
            if (index+1)==len(taxonomy['Taxon']):
                raise ValueError('The input taxonomy format is currently not supported.')

    for index, taxon in enumerate(df_copy_num['taxon']): # loop all the taxa
        if 'Unassigned' in taxon:
            continue

        for rank in ranks: # loop all the taxonomic ranks, from species to kingdom
            try: # check if the rank in the taxon
                taxa_rank = re.search(rank + '(.*?);', taxon)[1]
                try: # check if the rank match rrnDB database
                    copy_num = taxon2copynum[taxa_rank]
                    df_copy_num.iloc[index,1]=copy_num
                    break # go check next taxon
                except: # if not, move higher rank
                    continue
            except: # if not, move to higher rank
                continue

        for rank in ranks:
            try: # check if the lowest rank is in the taxon
                taxa_rank = re.search(rank + '(.*)', taxon)[1]
                try: # check if the rank match rrnDB database
                    copy_num = taxon2copynum[taxa_rank]
                    df_copy_num.iloc[index,1]=copy_num
                    break # go check next taxon
                except: # if not, move to higher rank
                    continue
            except: # if not, move to higher rank
                continue

    if database=='greengenes':
        for index, taxon in enumerate(df_copy_num['taxon']): # loop all the taxa
            if '; s__' in taxon:
                genus_species = re.search('; g__' + '(.*)', taxon)[1]
                genus_species = re.sub('; s__',' ', genus_species)

                try: # check if the rank match rrnDB database
                    copy_num = taxon2copynum[genus_species]
                    df_copy_num.iloc[index,1]=copy_num
                    continue # go check next taxon
                except: # if not, move to higher rank
                    pass

    asv2copynum = dict(zip(df_copy_num.index,df_copy_num['copy_number']))
    table_copy_num_normalized = (table/[asv2copynum[i] for i in table.columns])


    return table_copy_num_normalized
