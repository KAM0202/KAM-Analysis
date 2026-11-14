import csv
from pathlib import Path

out_dir = Path("data/reference")
out_dir.mkdir(parents=True, exist_ok=True)

FX_TO_EUR = {"EUR": 1.00, "GBP": 1.18, "USD": 0.92}
FX_TO_USD = {"EUR": 1.09, "GBP": 1.28, "USD": 1.00}

franchises = [
    {
        "Club_ID": "Como 1907",
        "League": "Serie A",
        "Local_Currency": "EUR",
        "Total_Revenue_Local": 65_000_000,
        "Matchday_Rev_Local": 12_500_000,
        "Commercial_Retail_Local": 24_500_000,
        "Broadcast_Rev_Local": 28_000_000,
        "Wages_Local": 29_500_000,
        "Amortization_Local": 11_125_000,
        "CapEx_Budget_Local": 18_000_000,
        "CapEx_Actual_Local": 18_450_000,
        "Framework": "UEFA SCR (70% Cap)",
        "Threshold_Pct": 0.70,
    },
    {
        "Club_ID": "Real Madrid",
        "League": "La Liga",
        "Local_Currency": "EUR",
        "Total_Revenue_Local": 1_045_000_000,
        "Matchday_Rev_Local": 248_000_000,
        "Commercial_Retail_Local": 482_000_000,
        "Broadcast_Rev_Local": 315_000_000,
        "Wages_Local": 412_000_000,
        "Amortization_Local": 123_000_000,
        "CapEx_Budget_Local": 120_000_000,
        "CapEx_Actual_Local": 116_500_000,
        "Framework": "UEFA SCR (70% Cap)",
        "Threshold_Pct": 0.70,
    },
    {
        "Club_ID": "Man Utd",
        "League": "Premier League",
        "Local_Currency": "GBP",
        "Total_Revenue_Local": 662_000_000,
        "Matchday_Rev_Local": 137_000_000,
        "Commercial_Retail_Local": 303_000_000,
        "Broadcast_Rev_Local": 222_000_000,
        "Wages_Local": 364_000_000,
        "Amortization_Local": 89_000_000,
        "CapEx_Budget_Local": 55_000_000,
        "CapEx_Actual_Local": 61_200_000,
        "Framework": "UEFA SCR / PSR (70% Cap)",
        "Threshold_Pct": 0.70,
    },
    {
        "Club_ID": "GSW",
        "League": "NBA",
        "Local_Currency": "USD",
        "Total_Revenue_Local": 780_000_000,
        "Matchday_Rev_Local": 275_000_000,
        "Commercial_Retail_Local": 315_000_000,
        "Broadcast_Rev_Local": 190_000_000,
        "Wages_Local": 176_500_000,
        "Amortization_Local": 22_500_000,
        "CapEx_Budget_Local": 25_000_000,
        "CapEx_Actual_Local": 24_100_000,
        "Framework": "NBA Second Apron ($188.9M)",
        "Threshold_Pct": 0.242,
    },
    {
        "Club_ID": "Bengals",
        "League": "NFL",
        "Local_Currency": "USD",
        "Total_Revenue_Local": 545_000_000,
        "Matchday_Rev_Local": 92_000_000,
        "Commercial_Retail_Local": 118_000_000,
        "Broadcast_Rev_Local": 335_000_000,
        "Wages_Local": 238_000_000,
        "Amortization_Local": 14_200_000,
        "CapEx_Budget_Local": 30_000_000,
        "CapEx_Actual_Local": 29_400_000,
        "Framework": "NFL Hard Cap ($255.4M)",
        "Threshold_Pct": 0.469,
    },
]

output_rows = []
for c in franchises:
    cur = c["Local_Currency"]
    fx_eur = FX_TO_EUR[cur]
    fx_usd = FX_TO_USD[cur]

    total_squad_cost_local = c["Wages_Local"] + c["Amortization_Local"]
    scr_ratio = round(total_squad_cost_local / c["Total_Revenue_Local"], 4)
    non_matchday_share = round((c["Commercial_Retail_Local"] + c["Broadcast_Rev_Local"]) / c["Total_Revenue_Local"], 4)
    capex_var_pct = round((c["CapEx_Actual_Local"] - c["CapEx_Budget_Local"]) / c["CapEx_Budget_Local"], 4)

    if scr_ratio >= c["Threshold_Pct"]:
        risk_flag = "BREACH / OVER THRESHOLD"
    elif scr_ratio >= (c["Threshold_Pct"] - 0.03):
        risk_flag = "WATCHLIST (WITHIN 3%)"
    else:
        risk_flag = "COMPLIANT / OPTIMAL"

    output_rows.append({
        "Club_ID": c["Club_ID"],
        "League": c["League"],
        "Local_Currency": cur,
        "Total_Revenue_Local": c["Total_Revenue_Local"],
        "Total_Revenue_EUR": round(c["Total_Revenue_Local"] * fx_eur, 2),
        "Total_Revenue_USD": round(c["Total_Revenue_Local"] * fx_usd, 2),
        "Total_Squad_Cost_Local": total_squad_cost_local,
        "Total_Squad_Cost_EUR": round(total_squad_cost_local * fx_eur, 2),
        "Total_Squad_Cost_USD": round(total_squad_cost_local * fx_usd, 2),
        "Squad_Cost_Ratio": scr_ratio,
        "Regulatory_Threshold": c["Threshold_Pct"],
        "Regulatory_Framework": c["Framework"],
        "Compliance_Flag": risk_flag,
        "Non_Matchday_Yield_Share": non_matchday_share,
        "CapEx_Variance_Pct": capex_var_pct,
    })

out_file = out_dir / "global_portfolio_etl.csv"
with open(out_file, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=output_rows[0].keys())
    writer.writeheader()
    writer.writerows(output_rows)

print(f"ETL Complete -> {out_file} ({len(output_rows)} franchises processed)")
for r in output_rows:
    print(f"  {r['Club_ID']:12s} | Rev: €{r['Total_Revenue_EUR']/1e6:6.1f}M | SCR: {r['Squad_Cost_Ratio']*100:5.1f}% | Status: {r['Compliance_Flag']}")