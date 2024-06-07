# Datasets Overview
This repository contains two datasets sourced from different sources:

## [Taiwan Open Government Data License](https://data.gov.tw/en): Emergency Department Visits

This dataset focuses on cases that visited emergency departments within Taiwan. It provides insights into the frequency, demographics, and reasons for emergency department visits.

## [European Centre for Disease Prevention and Control (ECDC)](https://www.ecdc.europa.eu/en/publications-data/data-mpox-monkeypox-cases-eueea): Monkeypox Cases in the EU/EEA

This dataset specifically focuses on monkeypox cases within the European Union and European Economic Area (EU/EEA). It offers valuable insights into the prevalence, distribution, and characteristics of monkeypox cases in this region.

# Installation
- Create environment for the required dependencies
```
conda create -n pytutorial python~=3.10.0
conda activate pytutorial
cd [CLONED_DIRECTORY]
pip install -r requirements.txt
```
- Buildup the src path
```
conda install conda-build
conda develop src
cd src
```

# Usage - Emergency Department Visits

## Loading a CSV File 
```
python
from er_visit import load_csv
df = load_csv([CLONED_DIRECTORY])
```

## Age and Gender Filter for ED Statistics
Gender: Females, Males, Total
Age: 5-year interval, start from 0 year old

```
from er_visit import parse_csv
new_df = parse_csv(df,'Males',[0,4])
```

## Plotting ED Statistics
bar chart
```
from er_visit import plot_er_stat
plot_er_stat(p=[CLONED_DIRECTORY],
gender='Females',
age_range=(0, 4),
rank=10)
```
