import os
import sys 
from os.path import join,dirname,exists
from ipdb import set_trace
from os import system
# from hetio.downloader import download
# from hetio.datasets import datasets_url

import psycopg2 
import pandas.io.sql as pdsql

# from hetio.datasets import scratch_dir
import pandas as pd


datasets_url = 'http://192.168.0.97/share/StandigmDB/datasets'
scratch_dir = '.'

def download(remote_dir=None, filename=None, local_dir=None, force=False):

    base_dir = dirname(__file__)

    if local_dir is None:
        local_dir = join(base_dir, '.')

    os.system('mkdir -p %s' % local_dir)
    remotepath = join(remote_dir, filename)
    savepath = join(local_dir, filename)

    if not exists(savepath) or force==True: 
        os.system('wget -O %s %s' % (savepath, remotepath))

    return savepath

    
def unzip(local_filename, target_dir=None):
    
    if target_dir == None: 
        target_dir = dirname(local_filename)

    os.system( "unzip -q -o %s -d %s" % (local_filename, target_dir))
    

def load(version='201710'):

    if version == '201710':
        return load_version201710()
    else: 
        assert False


def load_version201710():
    def load_structure():
        
        localfile = download(remote_dir=join(datasets_url,'drug_central','2017-10'), 
            filename='structures.smiles.tsv')
        
        dataset = pd.read_csv(localfile, sep='\t')

        return dataset 

    chkfile_1 = join(scratch_dir, 'chk-drugcentral-v201710-pharmaclass.csv')
    chkfile_2 = join(scratch_dir, 'chk-drugcentral-v201710-activeingredient.csv')
    chkfile_3 = join(scratch_dir, 'chk-drugcentral-v201710-act-table-fulll.csv')


    if exists(chkfile_2) and exists(chkfile_1) and exists(chkfile_3):
        pharma_class = pd.read_csv(chkfile_1) 
        active_ingredient = pd.read_csv(chkfile_2)
        act_table_full = pd.read_csv(chkfile_3)
    else: 
        conn_string = "host='localhost' port=54320 dbname='drugcentral' "
        conn_string+= "user='postgres' password='docker' "
        conn = psycopg2.connect(conn_string)

        pharma_class = pdsql.read_sql_query(
            "SELECT * FROM %s;" % 'pharma_class' , conn)
        
        active_ingredient = pdsql.read_sql_query(
            "SELECT * FROM %s;" % 'active_ingredient' , conn)
    
        act_table_full = pdsql.read_sql_query(
            "SELECT * FROM %s;" % 'act_table_full' , conn)

        pharma_class.to_csv(chkfile_1, index=False)
        active_ingredient.to_csv(chkfile_2, index=False)
        act_table_full.to_csv(chkfile_3, index=False)    

    return {
        'pharma_class': pharma_class, 
        'active_ingredient': active_ingredient, 
        'act_table_full': act_table_full, 
        'structures': load_structure()
        }


def test_run():    
    import pickle 
    dataset = load()
    with open(join(scratch_dir, 'prcessed-drugcentral-v201710.pkl'),'wb') as fobj:
        pickle.dump(dataset, fobj)

