from typing import Union, Tuple, Optional
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def load_csv(p: Union[Path, str]) -> pd.DataFrame:
    if isinstance(p, str):
        p = Path(p)

    if 'csv' in p.name:
        return pd.read_csv(p, encoding='utf-8')

    else:
        f = list(p.glob('*.csv'))
        if len(f) == 0:
            raise FileNotFoundError(f'no csv file under the {p}')
        elif len(f) == 1:
            return pd.read_csv(f[0], encoding='utf-8')
        else:
            raise RuntimeError(f'multiple csv files under the {p}')


def preprocess_data(p: Union[Path, str], save_path: Union[Path, str]) -> pd.DataFrame:
    df = load_csv(p)
    df = df.sort_values(['CountryExp'], ascending=False)
    df['DateRep'] = pd.to_datetime(df['DateRep'])
    date_min = df['DateRep'].min().strftime('%Y-%m-%d')
    date_max = df['DateRep'].max().strftime('%Y-%m-%d')
    df['DateRep'] = f'{date_min} to {date_max}'

    df = df.groupby(['CountryExp', 'CountryCode', 'Source', 'DateRep'])['ConfCases'].sum()
    df.to_csv('test.csv')

    df.to_csv(save_path)

    return df


if __name__ == '__main__':
    p = '../test_file/Data_on_monkeypox_cases_in_the_EU_EEA.csv'
    save_path = '../test_file/summary_disease_cases.csv'
    preprocess_data(p, save_path=save_path)
