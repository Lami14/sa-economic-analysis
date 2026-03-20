# 🇿🇦 South Africa Economic Analysis (2000–2023)

An exploratory data analysis of South Africa's macroeconomic indicators over 23 years — examining GDP trends, the load-shedding crisis, government debt, trade balance, unemployment and foreign investment using Python.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.x-11557c)
![Seaborn](https://img.shields.io/badge/Seaborn-0.13-4C72B0)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

---

## 📸 Sample Charts

> *(Add screenshots of your generated charts here)*

---

## 🔍 Key Findings

- 🔴 SA's GDP **peaked at $416bn in 2011** then declined — never recovering to that level
- ⚡ Load-shedding hours increased **24x between 2015 and 2023**, with a strong negative correlation to GDP growth
- 💸 Government debt **nearly doubled** from 46% to 84.7% of GDP over 23 years — breaching the IMF 60% warning threshold
- 👷 Unemployment **never fell below 22%** in 23 years, rising to 32.1% by 2023
- 📉 Two recessions: **2009** (global financial crisis) and **2020** (COVID-19)

---

## 📊 Charts Generated

| # | Chart | Description |
|---|---|---|
| 1 | GDP Trend | GDP in USD billions with recession shading |
| 2 | GDP Growth Rate | Annual growth bar chart — green/red coded |
| 3 | Inflation vs Unemployment | Dual-axis line chart |
| 4 | Trade Balance | Exports vs imports + surplus/deficit bars |
| 5 | Government Debt | Debt as % of GDP with IMF threshold line |
| 6 | Load-Shedding vs GDP | Hours of outages vs growth rate |
| 7 | FDI Inflows | Foreign direct investment over time |
| 8 | Correlation Heatmap | Pearson correlation between all indicators |

---

## 📁 Project Structure

```
sa-economic-analysis/
├── data/
│   └── sa_economic_data.csv        # 24 years of SA economic indicators
├── src/
│   ├── load_data.py                # Data loading and validation
│   ├── analyze_data.py             # Statistical and economic analysis
│   └── visualize_data.py           # All 8 chart generators
├── notebooks/
│   └── sa_economic_analysis.ipynb  # Full analysis notebook
├── outputs/                        # Generated charts (git-ignored)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

```bash
git clone https://github.com/Lami14/sa-economic-analysis.git
cd sa-economic-analysis
pip install -r requirements.txt

# Run the full analysis and generate all charts
python src/visualize_data.py

# Or open the notebook
jupyter notebook notebooks/sa_economic_analysis.ipynb
```

---

## 🛠️ Tech Stack

| Library | Purpose |
|---|---|
| `pandas` | Data loading, cleaning, transformation |
| `numpy` | Numerical calculations |
| `matplotlib` | All chart generation |
| `seaborn` | Correlation heatmap and styling |
| `jupyter` | Interactive notebook analysis |

---

## 💡 What I Learned

- How to source, clean and structure real macroeconomic time-series data
- Calculating and interpreting financial metrics — trade balance, debt ratios, correlation
- Communicating data insights as a narrative with clear business recommendations
- Building multi-panel and dual-axis charts for comparative analysis
- The real economic cost of infrastructure failure on a developing economy

---

## 🔮 Future Improvements

- [ ] Add provincial-level GDP and unemployment breakdown
- [ ] Build an interactive Plotly Dash dashboard
- [ ] Incorporate World Bank API for live data updates
- [ ] Add predictive modelling for GDP forecasting

---

*Built by [Lamla](https://github.com/Lami14) · South Africa Economic Analysis · Data Science Portfolio 🇿🇦*

