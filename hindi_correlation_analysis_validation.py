import pandas as pd
from scipy.stats import pearsonr

# 1. Load Data
df = pd.read_csv('Hindi_Transformed_Data_1.csv')

# 2. Individual Trial Correlation (276 pairs)
df_paired = df.pivot_table(index=['Participant_ID', 'Verb'],
                          columns='Task_Block',
                          values='Rating_Normalized').dropna()

r_trial, p_trial = pearsonr(df_paired['At-issueness'], df_paired['Projection'])

# 3. Aggregated Verb Correlation (12 verbs)
verb_means = df.groupby(['Verb', 'Task_Block'])['Rating_Normalized'].mean().unstack()

r_agg, p_agg = pearsonr(verb_means['At-issueness'], verb_means['Projection'])

# --- ADD THESE PRINT STATEMENTS TO SEE THE OUTPUT ---
print(f"--- Correlation Results ---")
print(f"Individual Trial Correlation (n={len(df_paired)} pairs):")
print(f"  Pearson's r: {r_trial:.4f}")
print(f"  p-value:     {p_trial:.4f}")

print(f"\nAggregated Verb Correlation (n={len(verb_means)} verbs):")
print(f"  Pearson's r: {r_agg:.4f}")
print(f"  p-value:     {p_agg:.4f}")
