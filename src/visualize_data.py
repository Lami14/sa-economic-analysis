"""
visualize_data.py
-----------------
Generates professional economic charts for South Africa's
macroeconomic indicators using Matplotlib and Seaborn.

Charts:
    1. GDP trend with recession shading
    2. GDP growth rate bar chart
    3. Inflation vs unemployment over time
    4. Trade balance surplus/deficit
    5. Government debt trajectory
    6. Load-shedding hours vs GDP growth
    7. FDI inflows over time
    8. Economic correlation heatmap
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# ── Style ──────────────────────────────────────────────────────
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor":   "white",
    "font.family":      "DejaVu Sans",
    "axes.titlesize":   13,
    "axes.titleweight": "bold",
    "axes.labelsize":   11,
})

SA_GREEN  = "#007A4D"
SA_GOLD   = "#FFB612"
SA_RED    = "#DE3831"
SA_BLUE   = "#002395"
GREY      = "#94a3b8"

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def _save(filename: str) -> None:
    path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    logger.info(f"Saved: {path}")


# ─────────────────────────────────────────────────────────────
# Chart 1: GDP Trend
# ─────────────────────────────────────────────────────────────
def plot_gdp_trend(df: pd.DataFrame) -> None:
    """Plot SA GDP in USD billions from 2000–2023 with recession shading."""
    fig, ax = plt.subplots(figsize=(12, 5))

    ax.fill_between(df["year"], df["gdp_usd_billions"],
                    alpha=0.15, color=SA_GREEN)
    ax.plot(df["year"], df["gdp_usd_billions"],
            color=SA_GREEN, linewidth=2.5, marker="o", markersize=4, label="GDP (USD Billions)")

    # Shade recession years
    recessions = [2009, 2020]
    for yr in recessions:
        ax.axvspan(yr - 0.5, yr + 0.5, alpha=0.15, color=SA_RED, label="Recession" if yr == 2009 else "")

    # Annotate peak
    peak_idx = df["gdp_usd_billions"].idxmax()
    ax.annotate(
        f"  Peak: ${df.loc[peak_idx, 'gdp_usd_billions']:.0f}bn",
        xy=(df.loc[peak_idx, "year"], df.loc[peak_idx, "gdp_usd_billions"]),
        fontsize=9, color=SA_GREEN, fontweight="bold"
    )

    ax.set_title("South Africa — GDP 2000–2023")
    ax.set_xlabel("Year")
    ax.set_ylabel("GDP (USD Billions)")
    ax.set_xticks(df["year"])
    plt.xticks(rotation=45)
    ax.legend()
    plt.tight_layout()
    _save("01_gdp_trend.png")


# ─────────────────────────────────────────────────────────────
# Chart 2: GDP Growth Rate
# ─────────────────────────────────────────────────────────────
def plot_gdp_growth(df: pd.DataFrame) -> None:
    """Bar chart of annual GDP growth rate, positive=green, negative=red."""
    fig, ax = plt.subplots(figsize=(12, 5))

    colours = [SA_GREEN if g >= 0 else SA_RED for g in df["gdp_growth_pct"]]
    bars = ax.bar(df["year"], df["gdp_growth_pct"], color=colours, alpha=0.85, width=0.7)

    ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
    ax.axhline(df["gdp_growth_pct"].mean(), color=SA_GOLD, linewidth=1.5,
               linestyle="--", label=f"Average: {df['gdp_growth_pct'].mean():.1f}%")

    ax.set_title("South Africa — Annual GDP Growth Rate 2000–2023")
    ax.set_xlabel("Year")
    ax.set_ylabel("GDP Growth (%)")
    ax.set_xticks(df["year"])
    plt.xticks(rotation=45)

    green_patch = mpatches.Patch(color=SA_GREEN, label="Growth")
    red_patch   = mpatches.Patch(color=SA_RED,   label="Contraction")
    ax.legend(handles=[green_patch, red_patch,
              plt.Line2D([0], [0], color=SA_GOLD, linestyle="--", label=f"Average")])
    plt.tight_layout()
    _save("02_gdp_growth.png")


# ─────────────────────────────────────────────────────────────
# Chart 3: Inflation vs Unemployment
# ─────────────────────────────────────────────────────────────
def plot_inflation_unemployment(df: pd.DataFrame) -> None:
    """Dual-line chart comparing inflation and unemployment over time."""
    fig, ax1 = plt.subplots(figsize=(12, 5))

    ax1.plot(df["year"], df["inflation_pct"], color=SA_RED,
             linewidth=2, marker="o", markersize=4, label="Inflation (%)")
    ax1.set_ylabel("Inflation (%)", color=SA_RED)
    ax1.tick_params(axis="y", labelcolor=SA_RED)

    ax2 = ax1.twinx()
    ax2.plot(df["year"], df["unemployment_pct"], color=SA_BLUE,
             linewidth=2, marker="s", markersize=4, label="Unemployment (%)")
    ax2.set_ylabel("Unemployment (%)", color=SA_BLUE)
    ax2.tick_params(axis="y", labelcolor=SA_BLUE)

    ax1.set_title("South Africa — Inflation vs Unemployment 2000–2023")
    ax1.set_xlabel("Year")
    ax1.set_xticks(df["year"])
    plt.xticks(rotation=45)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
    plt.tight_layout()
    _save("03_inflation_unemployment.png")


# ─────────────────────────────────────────────────────────────
# Chart 4: Trade Balance
# ─────────────────────────────────────────────────────────────
def plot_trade_balance(df: pd.DataFrame) -> None:
    """Stacked area chart of exports vs imports with trade balance."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    ax1.fill_between(df["year"], df["exports_usd_billions"],
                     alpha=0.4, color=SA_GREEN, label="Exports")
    ax1.fill_between(df["year"], df["imports_usd_billions"],
                     alpha=0.4, color=SA_RED, label="Imports")
    ax1.plot(df["year"], df["exports_usd_billions"], color=SA_GREEN, linewidth=1.5)
    ax1.plot(df["year"], df["imports_usd_billions"], color=SA_RED, linewidth=1.5)
    ax1.set_ylabel("USD Billions")
    ax1.set_title("South Africa — Exports vs Imports 2000–2023")
    ax1.legend()

    trade_balance = df["exports_usd_billions"] - df["imports_usd_billions"]
    colours = [SA_GREEN if x >= 0 else SA_RED for x in trade_balance]
    ax2.bar(df["year"], trade_balance, color=colours, alpha=0.8, width=0.7)
    ax2.axhline(0, color="black", linewidth=0.8)
    ax2.set_ylabel("Trade Balance (USD Billions)")
    ax2.set_title("Trade Balance — Surplus vs Deficit")
    ax2.set_xlabel("Year")
    plt.xticks(df["year"], rotation=45)
    plt.tight_layout()
    _save("04_trade_balance.png")


# ─────────────────────────────────────────────────────────────
# Chart 5: Government Debt
# ─────────────────────────────────────────────────────────────
def plot_government_debt(df: pd.DataFrame) -> None:
    """Line chart of government debt as % of GDP with danger zone shading."""
    fig, ax = plt.subplots(figsize=(12, 5))

    ax.fill_between(df["year"], df["government_debt_pct_gdp"],
                    alpha=0.12, color=SA_RED)
    ax.plot(df["year"], df["government_debt_pct_gdp"],
            color=SA_RED, linewidth=2.5, marker="o", markersize=4)

    # Danger zone line at 60%
    ax.axhline(60, color=SA_GOLD, linestyle="--", linewidth=1.5,
               label="60% IMF Warning Threshold")

    ax.set_title("South Africa — Government Debt as % of GDP 2000–2023")
    ax.set_xlabel("Year")
    ax.set_ylabel("Debt (% of GDP)")
    ax.set_xticks(df["year"])
    plt.xticks(rotation=45)
    ax.legend()
    plt.tight_layout()
    _save("05_government_debt.png")


# ─────────────────────────────────────────────────────────────
# Chart 6: Load-Shedding vs GDP Growth
# ─────────────────────────────────────────────────────────────
def plot_loadshedding_impact(df: pd.DataFrame) -> None:
    """Scatter + bar combo showing load-shedding hours vs GDP growth."""
    ls_df = df[df["loadshedding_hours_per_year"] > 0].copy()

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    ax1.bar(ls_df["year"], ls_df["loadshedding_hours_per_year"],
            color=SA_RED, alpha=0.8, width=0.6, label="Load-Shedding Hours")
    ax1.set_ylabel("Hours of Load-Shedding")
    ax1.set_title("South Africa — Load-Shedding Severity vs GDP Growth")
    ax1.legend()

    colours = [SA_GREEN if g >= 0 else SA_RED for g in ls_df["gdp_growth_pct"]]
    ax2.bar(ls_df["year"], ls_df["gdp_growth_pct"],
            color=colours, alpha=0.8, width=0.6)
    ax2.axhline(0, color="black", linewidth=0.8)
    ax2.set_ylabel("GDP Growth (%)")
    ax2.set_xlabel("Year")
    ax2.set_title("GDP Growth Rate During Load-Shedding Years")
    plt.xticks(ls_df["year"], rotation=45)
    plt.tight_layout()
    _save("06_loadshedding_gdp.png")


# ─────────────────────────────────────────────────────────────
# Chart 7: FDI Inflows
# ─────────────────────────────────────────────────────────────
def plot_fdi(df: pd.DataFrame) -> None:
    """Bar chart of foreign direct investment inflows."""
    fig, ax = plt.subplots(figsize=(12, 5))

    ax.bar(df["year"], df["fdi_usd_billions"],
           color=SA_BLUE, alpha=0.75, width=0.7)
    ax.axhline(df["fdi_usd_billions"].mean(), color=SA_GOLD,
               linestyle="--", linewidth=1.5,
               label=f"Average: ${df['fdi_usd_billions'].mean():.1f}bn")

    ax.set_title("South Africa — Foreign Direct Investment Inflows 2000–2023")
    ax.set_xlabel("Year")
    ax.set_ylabel("FDI (USD Billions)")
    ax.set_xticks(df["year"])
    plt.xticks(rotation=45)
    ax.legend()
    plt.tight_layout()
    _save("07_fdi_inflows.png")


# ─────────────────────────────────────────────────────────────
# Chart 8: Correlation Heatmap
# ─────────────────────────────────────────────────────────────
def plot_correlation_heatmap(df: pd.DataFrame) -> None:
    """Seaborn heatmap of Pearson correlations between economic indicators."""
    cols = [
        "gdp_growth_pct", "inflation_pct", "unemployment_pct",
        "government_debt_pct_gdp", "fdi_usd_billions",
        "loadshedding_hours_per_year"
    ]
    labels = [
        "GDP Growth", "Inflation", "Unemployment",
        "Govt Debt %", "FDI", "Load-Shedding"
    ]

    corr = df[cols].corr()
    corr.index   = labels
    corr.columns = labels

    fig, ax = plt.subplots(figsize=(9, 7))
    sns.heatmap(
        corr, annot=True, fmt=".2f",
        cmap="RdYlGn", center=0,
        vmin=-1, vmax=1,
        linewidths=0.5,
        ax=ax, annot_kws={"size": 10}
    )
    ax.set_title("South Africa — Economic Indicators Correlation Matrix")
    plt.tight_layout()
    _save("08_correlation_heatmap.png")


# ─────────────────────────────────────────────────────────────
# Run All Charts
# ─────────────────────────────────────────────────────────────
def generate_all_charts(df: pd.DataFrame) -> None:
    """Generate and save all 8 charts."""
    logger.info("Generating all charts...")
    plot_gdp_trend(df)
    plot_gdp_growth(df)
    plot_inflation_unemployment(df)
    plot_trade_balance(df)
    plot_government_debt(df)
    plot_loadshedding_impact(df)
    plot_fdi(df)
    plot_correlation_heatmap(df)
    logger.info(f"All charts saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    from load_data import load_economic_data
    df = load_economic_data("data/sa_economic_data.csv")
    generate_all_charts(df)
