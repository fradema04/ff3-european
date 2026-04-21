"""
download_data.py
Scarica e salva localmente i fattori FF3, WML e i prezzi azionari.
Eseguire una volta prima di usare i notebook.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.data_loader import load_ff3_europe, load_wml_europe, load_prices

START = '2010-01-01'
END   = '2026-02-28'

TICKERS = [
    'ASML.AS', 'SAP.DE', 'NESN.SW', 'NOVN.SW', 'ROG.SW',
    'MC.PA', 'SIE.DE', 'ALV.DE', 'BNP.PA', 'DTE.DE'
]

print("Downloading FF3 factors...")
ff3 = load_ff3_europe(start=START, end=END)
ff3.to_csv('raw/ff3_europe.csv')
print(f"  Saved: raw/ff3_europe.csv ({len(ff3)} rows)")

print("Downloading WML factor...")
wml = load_wml_europe(start=START, end=END)
wml.to_csv('raw/wml_europe.csv')
print(f"  Saved: raw/wml_europe.csv ({len(wml)} rows)")

print("Downloading stock prices...")
returns = load_prices(TICKERS, start=START, end=END)
returns.to_csv('raw/returns_europe.csv')
print(f"  Saved: raw/returns_europe.csv ({len(returns)} rows)")

print("\nDone. All data saved to data/raw/")