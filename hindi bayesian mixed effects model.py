pip install bambi arviz

import pandas as pd
import bambi as bmb
import arviz as az
import matplotlib.pyplot as plt

# 1. Load the data
df = pd.read_csv('Hindi_Transformed_Data_1.csv')

# 2. Prepare the "Wide" format
# To see if At-issueness predicts Projection, they must be in the same row
df_wide = df.pivot_table(index=['Participant_ID', 'Verb', 'Verb_Type'],
                          columns='Task_Block',
                          values='Rating_Beta').reset_index()

# Clean up column names (removing spaces/dashes for the formula)
df_wide.columns = ['Participant_ID', 'Verb', 'Verb_Type', 'At_issueness', 'Projection']

# 3. Define the Bayesian Mixed-Effects Beta Regression
# Formula: Projection is predicted by At-issueness.
# (1|Participant_ID): Each person gets their own baseline.
# (1|Verb): Each verb gets its own baseline.
model = bmb.Model(
    "Projection ~ At_issueness + (1|Participant_ID) + (1|Verb)",
    df_wide,
    family="beta"
)

# 4. Fit the model (This uses MCMC sampling)
# draws=2000: The number of "simulations" the AI runs to find the truth.
results = model.fit(draws=2000, tune=1000, target_accept=0.9)

# 5. Output the Results
print("--- Bayesian Model Summary ---")
summary = az.summary(results, var_names=["At_issueness"])
print(summary)

# 6. Visualize the "Posterior" (The probability distribution of your result)
az.plot_posterior(results, var_names=["At_issueness"])
plt.title("Probability Distribution of the At-issueness Effect")
plt.show()
