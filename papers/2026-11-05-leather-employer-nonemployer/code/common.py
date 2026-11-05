"""Shared paths, constants and loaders for paper 21 (employer vs nonemployer leather and allied product manufacturing)."""
import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
RAW = os.path.join(ROOT, 'data', 'raw')
RES = os.path.join(ROOT, 'results')
FIG = os.path.join(ROOT, 'figures')

CBP_FILE = os.path.join(RAW, 'cbp_naics316_us_2004_2023.csv')
NES_FILE = os.path.join(RAW, 'nonemp_naics316_us_2004_2024.csv')

# NAICS vintage assumed for each reference year (standard five-year cycle; the 2012 change is visible in the 6-digit codes
# present in the files, the others are assumed, see Methods)
def vintage(y):
    return 2002 if y <= 2007 else 2007 if y <= 2011 else 2012 if y <= 2016 else 2017 if y <= 2021 else 2022
BREAK_YEARS = [2008, 2012, 2017, 2022]          # first reference year of a new NAICS vintage
SIZE = ['n_lt5', 'n_5_9', 'n_10_19', 'n_20_49', 'n_50_99', 'n_100_249', 'n_250_499', 'n_500_999', 'n_1000plus']
SIZE_LAB = ['1-4*', '5-9', '10-19', '20-49', '50-99', '100-249', '250+']
MEASURE = {'00': 'All industries', '31-33': 'Manufacturing', '316': 'Leather and allied products (NAICS 316)'}

def load_cbp():
    d = pd.read_csv(CBP_FILE, dtype={'naics': str, 'empflag': str, 'emp_nf': str, 'qp1_nf': str, 'ap_nf': str})
    for c in SIZE:
        d[c] = pd.to_numeric(d[c], errors='coerce')     # 'N' -> NaN
    return d

def load_nes():
    return pd.read_csv(NES_FILE, dtype={'naics': str, 'estab_f': str, 'rcptot_n_f': str, 'rcptot_f': str, 'source': str})

def cagr(a, b, years):
    return (b / a) ** (1 / years) - 1
