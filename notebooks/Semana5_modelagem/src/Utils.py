import glob
import numpy as np
import pandas as pd
from time import strftime
import matplotlib.pyplot as plt


class LimpezaDados:

    def merge_csv_folder(prefix, path, memory='no'):

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


    def header_cleaner(df):

        """
        """
        cols = df.columns.str.strip().str.lower()
        trat1 = [col.replace(" ", '_') for col in cols]
        trat2 = [col.replace('.','') for col in trat1]
        return trat2

    def split_columns2(df, original, res1, res2, separator):

        """
        """
        df[[res1,res2]] = df[original].str.split(separator, expand = True)
        return df

    def df_filter(df, cond):

        """
        """
        new_df = df.filter(regex=cond)
        return new_df

    
    
    

class EDA:
    
    def analise_cat_1(df,var,label = '',fl_ordena=0, num = False, q = 0, q2 = 0, y = 'ratingValue_flag'):
        
        if label == '':
            label = var
        df_ = df.copy()
        if num:
            if q == 0:
                if q2 == 0:
                    df_[var+'_cat'] = pd.qcut(df_[var],q= [0.0,0.2,0.5,0.8,1.0],retbins=True,duplicates='drop')[0].cat.add_categories('missing')
                    var= var+'_cat'
                else:
                    df_[var+'_cat'] = pd.qcut(df_[var],q= q2,retbins=True,duplicates='drop')[0].cat.add_categories('missing')
                    var= var+'_cat'
            else :
                df_[var+'_cat'] = pd.cut(df_[var],bins=q).cat.add_categories('missing')
                var= var+'_cat'
        print('\n')
        print('Análise da variável {}'.format(var))
        print('# valores distintos {}'.format(df_[var].nunique()))
        try:
            df_[var] = df_[var].fillna('missing')
        except :
            df_[var] = df_[var].cat.add_categories('missing').fillna('missing')
        total_maus = df_[y].sum()
        total_bons = df_.shape[0] - df_[y].sum()
        def tx(x):
            return sum(x)*100/sum(1 -x +x)
        def pct(x):
            return sum(1-x+x)*1.0/ (df_.shape[0])
        def pct_maus(x):
            return (sum(x)/total_maus )
        def rr(x):
            return (sum(x)/total_maus )/(sum(1-x)/total_bons)
        def WoE(x):
            return np.log(rr(x))
        def IV(x):
            return -(sum(1-x)/total_bons - sum(x)/total_maus)*WoE(x)
        s = df_.groupby(var).agg({y: [np.size,pct,pct_maus, tx,rr,WoE,IV]})[y]
        def color_negative_green(val):
            color = 'red' if val < 0 else 'black'
            return 'color: %s' % color
        print('IV : {:.3f}'.format(s.IV.sum()))
        #print('Beta : {:.3f}'.format(dic_beta[var]))
        t = s.style.applymap(color_negative_green)
        display(pd.DataFrame(df_[var].value_counts()).join(pd.DataFrame(df_[var].value_counts(normalize= True)*100), lsuffix = 'k').rename(columns = {var+'k': '#', var: '%'}))
        display(t)
        by_var = df_.groupby(var).agg({y:[np.size, np.mean]})[y]
        if fl_ordena ==1 :
            by_var =  by_var.sort_values(by = 'mean')
        Y1 = by_var['size']
        Y2 = by_var['mean']
        Y_mean = np.ones(shape=(len(Y1.index)))* df_[y].mean()
        index =  np.arange(len(Y1.index))
        #with plt.style.context('my_custom_style'):
        if True:
            plt.bar(index,Y1,alpha = 0.3, color= 'gray')
            plt.grid(False)
            plt.xticks(rotation = 20         if var[:2] not in ( 'fl', 'cd')  else 0)
            plt.ylabel('# registros')
            plt.twinx()
            plt.gca().set_xticks(index)
            plt.gca().set_xticklabels([Y1.index[i] for i in index], rotation = 40)
            plt.plot(index,Y_mean,label=  'tx. média evento')
            plt.plot(index,Y2,marker = 'o',label=  'tx. evento')
            plt.gca().set_yticklabels([ ' {:.2f}%'.format( i*100) for i in plt.gca().get_yticks()])
            plt.grid(False)
            plt.title('Bivariada  {}'.format(label))
            plt.ylabel('tx. evento')
            plt.xlabel(label)
            if var[:2] in ( 'fl', 'cd'):
                plt.legend(loc= 9,bbox_to_anchor=(0.5, -0.1))
            else:
                plt.legend(loc= 9,bbox_to_anchor=(0.5, -0.35))
            plt.show()
            print('\n')
        return label,np.round(s.IV.sum(),3), np.round(s.rr.mean(),3)



