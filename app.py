import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set up clean styling configurations for our charts
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 11, 'figure.titlesize': 14})

# ========================================================
# STEP 1: ORACLE-STYLE SQL DATABASE LAYER (USING SQLITE3)
# ========================================================
print("Initializing connection to institutional risk database warehouse...")
# Create an in-memory SQL database
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

print("Executing DDL/DML SQL statements on CORE_BANKING_LEDGER...")
# Create production-representative commercial lending schema
cursor.execute("""
CREATE TABLE CORE_BANKING_LEDGER (
    LOAN_ID TEXT PRIMARY KEY,
    CUSTOMER_NAME TEXT,
    LOAN_PRODUCT TEXT,
    ORIGINAL_PRINCIPAL REAL,
    OUTSTANDING_BALANCE REAL,
    INTEREST_RATE_PCT REAL,
    TENOR_MONTHS INTEGER,
    DAYS_PAST_DUE INTEGER
);
""")

# Populate database table rows
records = [
    ('LN-26-001', 'Apex Capital Logistics', 'Term Loan', 5000000.00, 4100000.00, 6.50, 60, 0),
    ('LN-26-002', 'Alpha Infrastructure Group', 'Revolving Credit', 12500000.00, 11200000.00, 5.25, 48, 14),
    ('LN-26-003', 'Vanguard Medical Networks', 'Equipment Finance', 7800000.00, 1500000.00, 7.10, 36, 0),
    ('LN-26-004', 'Horizon Hospitality LLC', 'Commercial Mortgage', 3200000.00, 2950000.00, 8.00, 24, 95),
    ('LN-26-005', 'Beacon Real Estate Trust', 'Bridge Loan', 1500000.00, 1450000.00, 9.25, 12, 45),
    ('LN-26-006', 'Nexus Electronics Corp', 'Working Capital Line', 9500000.00, 8900000.00, 5.75, 18, 5)
]

cursor.executemany("INSERT INTO CORE_BANKING_LEDGER VALUES (?, ?, ?, ?, ?, ?, ?, ?);", records)
conn.commit()
print("SQL Database execution successful.")

# ========================================================
# STEP 2: DATA EXTRACTION LAYER
# ========================================================
print("\nExtracting transactional data records via database query query...")
sql_query = "SELECT * FROM CORE_BANKING_LEDGER;"

# Read the SQL query output stream instantly into a Pandas DataFrame table
df = pd.read_sql_query(sql_query, conn)
print("Data extracted successfully into Python Pandas DataFrame.")

# Close connection
conn.close()

# ========================================================
# STEP 3: FINANCIAL RISK COMPILATION LAYER
# ========================================================
print("Executing financial risk feature engineering modeling...")

# 1. Map dynamic probability of default metrics
df['PROBABILITY_OF_DEFAULT_PD'] = np.where(df['DAYS_PAST_DUE'] == 0, 0.015,
                                  np.where(df['DAYS_PAST_DUE'] <= 30, 0.080,
                                  np.where(df['DAYS_PAST_DUE'] <= 90, 0.350, 0.850)))

# 2. Assign standard institutional Basel-framework asset classification categories
df['ASSET_CLASSIFICATION'] = np.where(df['DAYS_PAST_DUE'] == 0, 'Standard - Performing',
                             np.where(df['DAYS_PAST_DUE'] <= 30, 'Special Mention',
                             np.where(df['DAYS_PAST_DUE'] <= 90, 'Substandard Asset', 'Non-Performing Asset')))

# 3. Calculate Expected Loss Provisions (Balance * PD * LGD at 45%)
df['EXPECTED_LOSS_PROVISION'] = (df['OUTSTANDING_BALANCE'] * df['PROBABILITY_OF_DEFAULT_PD'] * 0.45).round(2)

print("Pipeline execution complete. Generating executive visualization deck...\n")

# ========================================================
# STEP 4: INTERACTIVE VISUALIZATION LAYER (SEABORN)
# ========================================================
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Institutional Credit Risk & Portfolio Exposure Analysis', weight='bold')

# Chart 1: Asset Classification Breakdown (Horizontal Barplot)
sns.barplot(
    x="OUTSTANDING_BALANCE", 
    y="ASSET_CLASSIFICATION", 
    data=df, 
    estimator=sum, 
    errorbar=None, 
    palette="Blues_r", 
    ax=axes[0]
)
axes[0].set_title("Capital Exposure by Asset Risk Tier", weight='semibold')
axes[0].set_xlabel("Outstanding Balance ($)")
axes[0].set_ylabel("Asset Performance Classification")

# Chart 2: Expected Loss Reserves by Customer Profile (Vertical Barplot)
sns.barplot(
    x="CUSTOMER_NAME", 
    y="EXPECTED_LOSS_PROVISION", 
    data=df.sort_values(by="EXPECTED_LOSS_PROVISION", ascending=False), 
    palette="Oranges_r", 
    ax=axes[1]
)
axes[1].set_title("Required Financial Provisioning by Client Portfolio", weight='semibold')
axes[1].set_xlabel("Corporate Debtor")
axes[1].set_ylabel("Calculated Expected Financial Loss ($)")
axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=30, ha="right")

# Optimize rendering layouts and export the image layer cleanly for GitHub
plt.tight_layout()
plt.savefig('executive_risk_dashboard.png', dpi=300)
plt.show()
