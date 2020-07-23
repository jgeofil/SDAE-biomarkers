import pandas as pd
import os

FILE_NAME = 'GEO_data_batch_corr_final.csv'

pd.read_csv('csv/'+FILE_NAME, header=0, index_col=0).to_pickle('pd/'+os.path.splitext(FILE_NAME)[0])