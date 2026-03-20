j"""
analyze_data.py
---------------
Performs statistical and economic analysis on South Africa's
macroeconomic indicators dataset.

Analyses:
    - GDP trend and growth periods
    - Trade balance (exports vs imports)
    - Inflation vs unemployment relationship
    - Load-shedding economic impact
    - Debt trajectory
    - Decade-by-decade comparison
"""

import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def get_gdp_analysis(df: pd.DataFrame) -> dict:
    """
    Analyse GDP trends — peak, trough, best/worst growth years.

    Args:
        df: Economic indicators DataFrame.

    Returns:
        Dictionary of key GDP statistics.
    """
    best_growth_idx  = df["gdp_growth_pct"].idxmax()
    worst_growth_idx = df["gdp_growth_pct"].idxmin()

    return {
        "peak_gdp_usd_bn":       round(df["gdp_usd_billions"].max(), 1),
        "peak_gdp_year":         int(df.loc[df["gdp_usd_billions"].idxmax(), "year"]),
        "avg_gdp_growth":        round(df["gdp_growth_pct"].mean(), 2),
        "best_growth_year":      int(df.loc[best_growth_idx, "year"]),
        "best_growth_pct":       round(df.loc[best_growth_idx, "gdp_growth_pct"], 1),
        "worst_growth_year":     int(df.loc[worst_growth_idx, "year"]),
        "worst_growth_pct":      round(df.loc[worst_growth_idx, "gdp_growth_pct"], 1),
        "gdp_per_capita_2023":   round(df.loc[df["year"] == 2023, "gdp_per_capita_usd"].values[0], 2),
        "gdp_per_capita_2000":   round(df.loc[df["year"] == 2000, "gdp_per_capita_usd"].values[0], 2),
    }


def get_trade_balance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate trade balance (exports minus imports) per year.

    Args:
        df: Economic indicators DataFrame.

    Returns:
        DataFrame with year, exports, imports and trade_balance columns.
    """
    trade = df[["year", "exports_usd_billions", "imports_usd_billions"]].copy()
    trade["trade_balance"] = trade["exports_usd_billions"] - trade["imports_usd_billions"]
    trade["trade_status"]  = trade["trade_balance"].apply(
        lambda x: "Surplus" if x > 0 else "Deficit"
    )
    return trade


def get_loadshedding_impact(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyse the relationship between load-shedding hours and GDP growth.

    Args:
        df: Economic indicators DataFrame.

    Returns:
        DataFrame of years with load-shedding > 0, sorted by severity.
    """
    ls = df[df["loadshedding_hours_per_year"] > 0][
        ["year", "loadshedding_hours_per_year", "gdp_growth_pct",
         "gdp_usd_billions", "electricity_production_gwh"]
    ].copy()

    ls["gdp_lost_estimate_bn"] = round(
        ls["loadshedding_hours_per_year"] * 0.45, 1  # ~$450M per 1000 hours estimate
    )
    return ls.sort_values("loadshedding_hours_per_year", ascending=False).reset_index(drop=True)


def get_debt_trajectory(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyse government debt as a percentage of GDP over time.

    Args:
        df: Economic indicators DataFrame.

    Returns:
        DataFrame with debt trajectory and year-on-year change.
    """
    debt = df[["year", "government_debt_pct_gdp"]].copy()
    debt["yoy_change"] = debt["government_debt_pct_gdp"].diff().round(2)
    debt["trend"] = debt["yoy_change"].apply(
        lambda x: "↑ Rising" if x > 0 else ("↓ Falling" if x < 0 else "→ Stable")
        if pd.notna(x) else "—"
    )
    return debt


def get_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute Pearson correlation between key economic indicators.

    Args:
        df: Economic indicators DataFrame.

    Returns:
        Correlation matrix as a DataFrame.
    """
    cols = [
        "gdp_growth_pct", "inflation_pct", "unemployment_pct",
        "government_debt_pct_gdp", "fdi_usd_billions",
        "loadshedding_hours_per_year", "electricity_production_gwh"
    ]
    return df[cols].corr().round(2)


def get_decade_comparison(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compare average economic indicators across decades.

    Args:
        df: Economic indicators DataFrame.

    Returns:
        DataFrame with decade-averaged indicators.
    """
    df = df.copy()
    df["decade"] = (df["year"] // 10 * 10).astype(str) + "s"

    return df.groupby("decade").agg(
        avg_gdp_growth     =("gdp_growth_pct",          "mean"),
        avg_unemployment   =("unemployment_pct",         "mean"),
        avg_inflation      =("inflation_pct",            "mean"),
        avg_debt_pct_gdp   =("government_debt_pct_gdp",  "mean"),
        avg_fdi            =("fdi_usd_billions",         "mean"),
        total_ls_hours     =("loadshedding_hours_per_year", "sum")
    ).round(2).reset_index()


def print_key_findings(df: pd.DataFrame) -> None:
    """Print a formatted summary of key economic findings."""
    gdp   = get_gdp_analysis(df)
    trade = get_trade_balance(df)
    ls    = get_loadshedding_impact(df)

    surplus_years = len(trade[trade["trade_status"] == "Surplus"])
    deficit_years = len(trade[trade["trade_status"] == "Deficit"])
    total_ls_hours = int(df["loadshedding_hours_per_year"].sum())

    print("\n🇿🇦 South Africa — Key Economic Findings (2000–2023)")
    print("=" * 58)
    print(f"\n📈 GDP")
    print(f"   Peak GDP         : ${gdp['peak_gdp_usd_bn']}bn ({gdp['peak_gdp_year']})")
    print(f"   Avg Growth Rate  : {gdp['avg_gdp_growth']}% per year")
    print(f"   Best Year        : {gdp['best_growth_year']} ({gdp['best_growth_pct']}%)")
    print(f"   Worst Year       : {gdp['worst_growth_year']} ({gdp['worst_growth_pct']}%)")
    print(f"   GDP/Capita 2000  : ${gdp['gdp_per_capita_2000']:,.0f}")
    print(f"   GDP/Capita 2023  : ${gdp['gdp_per_capita_2023']:,.0f}")

    print(f"\n🔁 Trade Balance")
    print(f"   Surplus years    : {surplus_years}")
    print(f"   Deficit years    : {deficit_years}")

    print(f"\n⚡ Load-Shedding")
    print(f"   Total hours lost : {total_ls_hours:,} hours (2008–2023)")
    print(f"   Worst year       : {int(ls.iloc[0]['year'])} ({int(ls.iloc[0]['loadshedding_hours_per_year']):,} hours)")
    print("=" * 58)


if __name__ == "__main__":
    from load_data import load_economic_data
    df = load_economic_data("data/sa_economic_data.csv")
    print_key_findings(df)
    print("\nCorrelation Matrix:")
    print(get_correlation_matrix(df))
  
