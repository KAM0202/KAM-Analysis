import csv, random
from pathlib import Path

base_path = Path.home() / 'Desktop' / 'sports-exec-dashboard' / 'data' / 'reference'
base_path.mkdir(parents=True, exist_ok=True)

with open(base_path / 'como_squad_wages_proxy.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['Player_ID', 'Department', 'Annual_Wage_EUR', 'Amortization_EUR', 'Contract_Expiry'])
    for i in range(1, 26):
        w.writerow([f"Player_{i}", 'First Team', random.randint(300000, 2500000), random.randint(100000, 1500000), random.randint(2025, 2029)])

with open(base_path / 'como_retail_skus.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['SKU_Category', 'Units_Sold_YTD', 'Avg_Margin_EUR', 'Total_Yield_EUR'])
    for cat in ['Adidas Lifestyle', 'Matchday Kit', 'Luxury Collab (Brioni)', 'Accessories']:
        u, m = random.randint(5000, 50000), round(random.uniform(15.0, 85.0), 2)
        w.writerow([cat, u, m, round(u * m, 2)])

with open(base_path / 'sinigaglia_capex_budget.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['Project_Phase', 'Allocated_Budget_EUR', 'Actual_Spend_EUR', 'Status'])
    for p in ['DO    for p in ['DO    for p in ['DO    for 'Lak    for p in ['DO    for p in ['DO    for p in ['DO    for 'Lak    for p 00    for p in ['DO t(b * random.uniform(0.85, 1.12))
        w.writerow([p, b, a, 'Over Budget' if a > b else 'On Track'])

print("Saved directly to:", base_path)
