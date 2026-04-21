"""
factor_model.py
Stima OLS di modelli fattoriali, rolling betas e alpha cumulativo.
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm


def estimate_factor_model(returns: pd.DataFrame,
                           factors: pd.DataFrame,
                           rf: pd.Series) -> pd.DataFrame:
    """
    Stima un modello fattoriale OLS per ogni titolo.

    Args:
        returns: DataFrame di rendimenti giornalieri (titoli in colonne)
        factors: DataFrame dei fattori (es. Mkt-RF, SMB, HML, WML)
        rf: Serie del risk-free rate giornaliero

    Returns:
        DataFrame con alpha, beta, t-stat e R² per ogni titolo
    """
    results = {}
    for ticker in returns.columns:
        y = returns[ticker] - rf
        X = sm.add_constant(factors)
        model = sm.OLS(y, X).fit()

        results[ticker] = {
            'alpha': model.params['const'],
            't_alpha': model.tvalues['const'],
            'R2': model.rsquared
        }
        for factor in factors.columns:
            results[ticker][f'beta_{factor}'] = model.params[factor]

    return pd.DataFrame(results).T.round(3)


def rolling_factor_model(return_series: pd.Series,
                          factors: pd.DataFrame,
                          rf: pd.Series,
                          window: int = 252) -> pd.DataFrame:
    """
    Stima rolling OLS su finestra mobile per un singolo titolo.

    Args:
        return_series: Serie rendimenti del titolo
        factors: DataFrame dei fattori
        rf: Serie risk-free rate
        window: ampiezza finestra in giorni (default 252)

    Returns:
        DataFrame con parametri rolling nel tempo
    """
    y_full = return_series - rf
    X_full = sm.add_constant(factors)
    rolling_params = []

    for i in range(window, len(y_full)):
        y_w = y_full.iloc[i - window:i]
        X_w = X_full.iloc[i - window:i]
        model_w = sm.OLS(y_w, X_w).fit()
        row = {'date': y_full.index[i], 'alpha': model_w.params['const']}
        for factor in factors.columns:
            row[f'beta_{factor}'] = model_w.params[factor]
        rolling_params.append(row)

    return pd.DataFrame(rolling_params).set_index('date')


def cumulative_alpha(returns: pd.DataFrame,
                      factors: pd.DataFrame,
                      rf: pd.Series) -> pd.DataFrame:
    """
    Calcola l'alpha cumulativo per ogni titolo.

    Returns:
        DataFrame con alpha cumulativo (in %) per ogni titolo
    """
    cum_alphas = {}
    for ticker in returns.columns:
        y = returns[ticker] - rf
        X = sm.add_constant(factors)
        model = sm.OLS(y, X).fit()
        daily_alpha = model.resid + model.params['const']
        cum_alphas[ticker] = ((1 + daily_alpha).cumprod() - 1) * 100

    return pd.DataFrame(cum_alphas)