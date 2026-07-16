# Bank Credit Risk & Data Pipeline
## Using SQL and Python to Catch Risky Loans and Calculate Financial Loss

### 💼 Why I Built This
With 7+ years of experience working inside corporate banking databases, I built this project to show how real financial institutions track loan data. It connects a database layout (SQL) with math analytics (Python) to help bank managers make smart, data-driven safety decisions.

### 🧠 The Banking Math Used
Instead of just looking at regular bank balances, this system uses real-world banking rules (Basel framework) to protect the bank from losing money:

1. **Loan Tracking:** Looks at how many days a customer is late on a payment (`DAYS_PAST_DUE`) and tags the loan as Safe, Risky, or Non-Performing.
2. **Probability of Default (PD):** Calculates the percentage chance that a customer will completely stop paying.
3. **Expected Loss:** Uses a standard banking formula to figure out exactly how much money the bank might lose if a client defaults:
   $$\text{Expected Loss} = \text{Outstanding Balance} \times \text{Chance of Default (PD)} \times \text{Loss Percentage (LGD)}$$

### 🛠️ The Tools Used
* **Database:** SQL (`sqlite3`) to create tables and store loan records.
* **Data Processing:** Python (`Pandas` and `NumPy`) to handle calculations.
* **Charts & Visuals:** Python (`Seaborn` and `Matplotlib`) to automatically build graphs.

### 📊 How the Data Flows
1. **SQL Layer:** We build a bank ledger table holding information for corporate clients (like loan amount, interest rates, and late days).
2. **Python Layer:** Python extracts the tables using SQL commands and runs our risk formulas across every single customer row.
3. **Visual Layer:** The system creates a dual-chart dashboard showing the final risk results automatically.

### 📈 Reading the Final Charts
* **Left Chart (Capital Exposure):** Shows the bank executives exactly where their money is tied up. It warns them that over $20 Million is sitting in a risky, late-paying bucket.
* **Right Chart (Expected Loss Reserves):** Instantly highlights the most dangerous client. For example, **Horizon Hospitality LLC** stands out because they are over 90 days late, meaning the bank needs to prepare over $1 Million in cash reserves to back up this single account.
<img width="4800" height="1800" alt="executive_risk_dashboard" src="https://github.com/user-attachments/assets/fabc445e-e8c2-4065-b5d8-d6916e741b4b" />
