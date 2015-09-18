
import tushare as ts
import pandas as pd
import os

class WrapperTushare:
    def __getattr__(self, attr):
        if ts.__dict__.has_key(attr):
            def default_method(*args,**kwargs):
                args_str = "-".join([str(i) for i in args])
                kwargs_str = "-".join(["_".join([k,str(w)]) for (k,w) in kwargs.items()])
                filename = "-".join([i for i in [attr,args_str,kwargs_str,"cache.csv"] if len(i) > 0] )
                data = self._read_cache(filename)
                if data is None:
                    data = ts.__dict__[attr](*args,**kwargs)
                    if isinstance(data, pd.DataFrame):
                        self._write_cache(data,filename)
                return data
            return default_method
            


    def _write_cache(self,df,fileName):
        file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'data','cache',fileName)
        if isinstance(df, pd.DataFrame):
            df.to_csv(file_path,index=False,encoding='utf-8')
        else:
            raise RuntimeError('data type is incorrect')
    

    def _read_cache(self,fileName):
        file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'data','cache',fileName)
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            if isinstance(df, pd.DataFrame) and 'code' in df.columns:
                df['code'] = df['code'].map(lambda x:str(x).zfill(6))
            return df
        else:
            return None
    def get_stock_basics(self):
        df = self._read_cache("get_stock_basics-cache.csv")
        if isinstance(df, pd.DataFrame) and 'code' in df.columns:
            df['code'] = df['code'].map(lambda x:str(x).zfill(6))
            df = df.set_index('code')
        return df
if __name__ == '__main__':
    w = WrapperTushare()
    data = w.get_debtpaying_data(2014,3)
    print data
    '''
    data = w.get_hist_data('600848')
    print data
    data = w.get_hist_data('600848',start='2015-01-05',end='2015-01-09')
    print data
    '''
