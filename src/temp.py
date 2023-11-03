from typing import Union, Tuple, Optional
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.axes import Axes

plt.rcParams['font.sans-serif'] = [
    'Arial Unicode MS']  # font supports a wide range of Unicode characters, including Chinese.
plt.rcParams['axes.unicode_minus'] = False  # default minus sign to ASCII '-' instead of Unicode '−'.


def load_csv(p: Union[Path, str]) -> pd.DataFrame:
    """
    load csv file

    :param p: csv path or containing folder
    :return:
        pd.DataFrame
    """
    if isinstance(p, str):  # if the variable p is an instance of the str class
        p = Path(p)  # if yes, creates a new object of 'Path' class and assigns it to the variable 'p'

    if 'csv' in p.name:
        return pd.read_csv(p, encoding='utf-8')  # If the 'csv in the p.name--> read this csv file. If the string "csv"
        # is not in the "name" attribute, this block of code will not execute and the function will return nothing
        # or continue with the next step of code.

    else:
        f = list(p.glob('*.csv'))  # To check if there is any csv file present in the path p or not by using glob method
        # and return a list of all the csv files stored in 'p'
        if len(f) == 0:
            raise FileNotFoundError(f'no csv file under the {p}')
        elif len(f) == 1:
            return pd.read_csv(f[0], encoding='utf-8')
        else:
            raise RuntimeError(f'multiple csv files under the {p}')


def parse_csv(df: pd.DataFrame,
              gender: str,
              age_range: Optional[Tuple[int, int]] = None) -> pd.DataFrame:
    """
    translate, select ages and gender from raw dataframe

    :param df:
    :param gender: {'M', 'F'}
    :param age_range: whether specify the range of ages
    :return: df
    """

    df.columns = ["Gender", "Age", "Diseases", "Patients"]
    df["Gender"].replace({"女": "Females", "男": "Males", "總計": "Total"}, inplace=True)
    df["Age"].replace({"總計": "Total"}, inplace=True)

    # age mask
    if age_range is None:
        age_m = df['Age'] == "Total"
    else:
        if age_range[0] != 85:
            age_m = df['Age'] == f'{age_range[0]}~{age_range[1]} year-old'
        else:  # above 85 years
            age_m = df['Age'] == f'{age_range[0]} greater than 85 year-old'

    df = df[age_m]

    # gender mask
    gm = df['Gender'] == gender
    df = df[gm].sort_values(['Patients'], ascending=False)
    total_pt = df['Patients'].max()
    df["Consultation rate(%)"] = df["Patients"] / total_pt * 100
    return df


def _plot_bar(ax: Axes, df: pd.DataFrame, gender: str):
    """bar plot"""
    x = df['Diseases'].to_numpy()
    y = df['Consultation rate(%)'].to_numpy()

    for i in range(df.shape[0]):
        ax.bar(x[i], y[i], label=x[i])

    ax.get_xaxis().set_visible(False)
    ax.set_ylabel('Consultation rate(%)')
    ax.set_title(f'Statistics of {gender} patients in ER')
    ax.legend()
    plt.show()


def plot_er_stat(p: Union[Path, str],
                 gender: str,
                 age_range: Optional[Tuple[int, int]] = None,
                 rank: int = 10):
    """

    :param p: csv path or containing folder
    :param gender: {'M', 'F'}
    :param age_range: whether specify the range of ages
    :param rank: top rank sorted by `Patients` numbers
    :return:
    """

    df = load_csv(p)
    df = parse_csv(df, gender, age_range)
    df = df[1:rank + 1]  # remove sum

    _, ax = plt.subplots()
    _plot_bar(ax, df, gender)


if __name__ == '__main__':
    plot_er_stat(
        p='../test_file/Summary_of_patients_in_ER_20210318.csv',
        gender='Females',
        age_range=None,
        rank=10
    )
