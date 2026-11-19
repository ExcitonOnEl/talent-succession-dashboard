from pathlib import Path
import numpy as np
import pandas as pd

script_dir = Path(__file__).parent
file_path = script_dir / 'WA_Fn-UseC_-HR-Employee-Attrition.csv'

df = pd.read_csv(file_path)

# A. Drop constant/useless columns found during EDA
cols_to_drop = ['EmployeeCount', 'Over18', 'StandardHours']
df = df.drop(columns=cols_to_drop)

# B. Calculate numerical metrics using eval()
# Stagnation Ratio: Years waiting for promotion relative to years in current role
df = df.eval(
    'Stagnation_Ratio = YearsSinceLastPromotion / (YearsInCurrentRole + 1)'
)

# Combined Performance Score: Blending PerformanceRating (3-4) and PercentSalaryHike (11-25)
df = df.eval('Perf_Composite = (PerformanceRating * 10) + PercentSalaryHike')

# C. Create 3-Tier Performance Label (for 9-Box Y-Axis)
df['Performance_Tier'] = np.where(
    df['Perf_Composite'] >= 58,
    '3 - High Performance',
    np.where(
        df['Perf_Composite'] >= 45,
        '2 - Moderate Performance',
        '1 - Developing Performance',
    ),
)

# D. Create 3-Tier Potential/Involvement Label (for 9-Box X-Axis)
df['Potential_Tier'] = np.where(
    df['JobInvolvement'] == 4,
    '3 - High Potential',
    np.where(
        df['JobInvolvement'] == 3,
        '2 - Moderate Potential',
        '1 - Low Potential',
    ),
)

# E. Create Succession Readiness Status
df['Succession_Readiness'] = np.where(
    (df['Performance_Tier'] == '3 - High Performance')
    & (df['Potential_Tier'] == '3 - High Potential')
    & (df['YearsInCurrentRole'] >= 2),
    'Ready Now',
    np.where(
        (df['Performance_Tier'].isin(['3 - High Performance', '2 - Moderate Performance']))
        & (df['Potential_Tier'].isin(['3 - High Potential', '2 - Moderate Potential'])),
        'Ready in 1-2 Years',
        'Needs Development',
    ),
)

# F. Create Human-Readable Job Level Labels
df['Level_Name'] = np.where(
    df['JobLevel'] == 1,
    'L1 - Staff',
    np.where(
        df['JobLevel'] == 2,
        'L2 - Senior Staff',
        np.where(
            df['JobLevel'] == 3,
            'L3 - Manager',
            np.where(
                df['JobLevel'] == 4, 'L4 - Senior Manager', 'L5 - Executive'
            ),
        ),
    ),
)

# G. Flag High-Risk Stagnant Talent (Active top/solid performers waiting 3+ years)
df['Stagnation_Risk_Flag'] = np.where(
    (df['Attrition'] == 'No')
    & (df['YearsSinceLastPromotion'] >= 3)
    & (df['Performance_Tier'] != '1 - Developing Performance'),
    'High Risk',
    'Normal',
)

# Round decimal columns for cleaner display in Power BI
df['Stagnation_Ratio'] = df['Stagnation_Ratio'].round(2)

# LOAD: Verify & Export to CSV
# ==========================================
# Quick check of the transformed columns
print('Transformed Data Shape:', df.shape)
print(
    df[[
        'EmployeeNumber',
        'Department',
        'Level_Name',
        'Performance_Tier',
        'Potential_Tier',
        'Succession_Readiness',
        'Stagnation_Risk_Flag',
    ]].head()
)

# Export clean dataset for Power BI
df.to_csv('HR_People_Dev_Ready.csv', index=False)
print("\nETL Complete! File 'HR_People_Dev_Ready.csv' is ready for Power BI.")

