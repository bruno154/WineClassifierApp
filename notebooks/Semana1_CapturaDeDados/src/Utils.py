import glob
import pandas as pd
from time import strftime


class LimpezaDados:

    def merge_csv_folder(self,prefix, path, memory='no'):

        """
        """
        if path == '':
            path = input("Por favor digite o endereços dos arquivos?\n")
        path = path.replace('\\','/')
        if path[:-1] != '/':
            path = path + '/'

        file_list = glob.glob(path + '*.csv')

        combined = pd.concat([pd.read_csv(f) for f in file_list])
        if memory == 'no':
            combined.to_csv(path + 'combined_{}_{}.csv'.format(prefix, strftime("%Y%m%d-%H%M%S")), index=False)
        else:
            return combined
        print('Feito')


    def header_cleaner(self, df):

        """
        """
        cols = df.columns.str.strip().str.lower()
        trat1 = [col.replace(" ", '_') for col in cols]
        trat2 = [col.replace('.','') for col in trat1]
        return trat2

    def split_columns(self, df, original, res1, res2, separator):

        """
        """
        df[[res1,res2]] = df[original].str.split(separator, expand = True)
        return df

    def df_filter(self, df, cond):

        """
        """
        new_df = df.filter(regex=cond)
        return new_df




