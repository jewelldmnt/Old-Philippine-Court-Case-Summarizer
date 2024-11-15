import pdfplumber
import pandas as pd
from scipy.stats import ttest_rel


def extract_table_from_pdf(pdf_path):
    data = []
    columns = ["GR Title", "Recall", "Precision", "F1"]
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    # Skip header rows
                    if row[0] == "GR Title":
                        continue
                    data.append(row)
    
    # Create DataFrame
    df = pd.DataFrame(data, columns=columns)
    
    # Convert numeric columns to float
    numeric_columns = ["Recall", "Precision", "F1"]
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

# Extract data from the PDFs
summit_scores = "Rouge_Scores/Summit_ROUGE_Scores.pdf"
lsatp_scores = "Rouge_Scores/LSATP_ROUGE_Scores.pdf"

df1 = extract_table_from_pdf(summit_scores)
df2 = extract_table_from_pdf(lsatp_scores)

# Ensure both DataFrames are aligned
if not df1["GR Title"].equals(df2["GR Title"]):
    raise ValueError("GR Titles in the two PDFs do not match. Align data before proceeding.")

# Perform paired t-tests
metrics = ["Recall", "Precision", "F1"]
results = {}

for metric in metrics:
    # Perform t-test
    t_stat, p_value = ttest_rel(df2[metric], df1[metric])  # LSATP - Summit
    mean_difference = df2[metric].mean() - df1[metric].mean()
    
    # Store results
    results[metric] = {
        "t-statistic": t_stat,
        "p-value": p_value,
        "mean difference": mean_difference
    }

# Display results
for metric, result in results.items():
    print(f"{metric}:")
    print(f"  Mean Difference = {result['mean difference']:.4f}")
    print(f"  t-statistic = {result['t-statistic']:.4f}")
    print(f"  p-value = {result['p-value']:.4f}")
    
    # Interpretation
    if result["p-value"] < 0.05:
        if result["mean difference"] > 0:
            print(f"  Positive significant difference: LSATP is better in {metric}.")
        else:
            print(f"  Negative significant difference: Summit is better in {metric}.")
    else:
        print(f"  No significant difference in {metric}.")