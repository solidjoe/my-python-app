import pandas as pd
import numpy as np

# 1. LOAD THE DATA

FILE_PATH = '/content/Hindi_Transformed_Data_Final.xlsx'

try:

    df = pd.read_excel(FILE_PATH)
    print("✅ File loaded successfully.\n")
except Exception as e:
    print(f"❌ Error: Could not find or read the file. {e}")

    raise

#  2. CALCULATE SD PER SESSION
# This calculates the Standard Deviation of the 'Rating' for each block (12 items)
session_variances = df.groupby(['Participant_ID', 'Task_Block'])['Rating'].std().reset_index()
session_variances.columns = ['Participant_ID', 'Task_Block', 'Response_SD']

#  3. CALCULATE GROUP METRICS
# We find the average 'volatility' of the whole group
group_mean = session_variances['Response_SD'].mean()
group_std  = session_variances['Response_SD'].std()

# 4. DEFINE THE ZOMBIE THRESHOLD
# Logic: 3 Standard Deviations below the mean (searching for 'flatliners')
threshold = group_mean - (3 * group_std)

print(f"📊 Average Participant SD: {group_mean:.2f}")
print(f"📊 Group SD of Variances: {group_std:.2f}")
print(f"🚫 Zombie Threshold (3SD below mean): {threshold:.2f}")
print("-" * 30)

#  5. IDENTIFY THE ZOMBIES
zombies = session_variances[session_variances['Response_SD'] < threshold]

if len(zombies) > 0:
    print(f"🧟 Found {len(zombies)} Zombie Session(s):")
    print(zombies)
else:
    print("✅ No Zombies found! All participants moved the sliders sufficiently.")

# Optional: Show the top 5 most 'consistent' (potential low variance) participants
print("\n🔍 Most 'Flat' Responders (Lowest SD):")
print(session_variances.sort_values(by='Response_SD').head())
