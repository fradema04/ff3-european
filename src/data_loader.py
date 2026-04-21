"""
data_loader.py
Funzioni per scaricare e pulire i fattori Fama-French e i prezzi azionari.
"""

import pandas as pd
import yfinance as yf


def load_ff3_europe(start: str = None, end: str = None) -> pd.DataFrame:
    """
    Scarica i fattori Fama-French 3-factor Europa giornalieri
    dalla Kenneth French Data Library.
    
    Returns:
        DataFrame con colonne: Mkt-RF, SMB, HML, RF
    """
    url = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Europe_3_Factors_daily_CSV.zip"
    raw = pd.read_csv(url, skiprows=6, index_col=0, dtype=str)
    df = raw[raw.index.str.strip().str.match(r'^\d{8}$')].copy()
    df.index = pd.to_datetime(df.index.str.strip(), format='%Y%m%d')
    df.columns = df.columns.str.strip()
    df = df.astype(float) / 100

    if start:
        df = df[df.index >= start]
    if end:
        df = df[df.index <= end]

    return df


def load_wml_europe(start: str = None, end: str = None) -> pd.DataFrame:
    """
    Scarica il fattore momentum (WML) Europa giornaliero
    dalla Kenneth French Data Library.

    Returns:
        DataFrame con colonna: WML
    """
    url = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Europe_MOM_Factor_daily_CSV.zip"
    raw = pd.read_csv(url, skiprows=6, index_col=0, dtype=str)
    df = raw[raw.index.str.strip().str.match(r'^\d{8}$')].copy()
    df.index = pd.to_datetime(df.index.str.strip(), format='%Y%m%d')
    df.columns = df.columns.str.strip()
    df = df.astype(float) / 100
    df.columns = ['WML']

    if start:
        df = df[df.index >= start]
    if end:
        df = df[df.index <= end]

    return df


def load_prices(tickers: list, start: str, end: str) -> pd.DataFrame:
    """
    Scarica prezzi adjusted giornalieri da Yahoo Finance
    e calcola i rendimenti semplici.

    Returns:
        DataFrame di rendimenti giornalieri
    """
    prices = yf.download(tickers, start=start, end=end, auto_adjust=True)['Close']
    returns = prices.pct_change().dropna()
    return returns