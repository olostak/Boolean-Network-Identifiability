import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV files
df1 = pd.read_csv('./evaluate/cell_division/banchmarks.csv')  # Replace 'file1.csv' with your first file name
df2 = pd.read_csv('./evaluate/mir-9-neurogeneses/banchmarks.csv')  # Replace 'file2.csv' with your second file name
df3 = pd.read_csv('./evaluate/tumor_cell_invasion_and_migration/banchmarks.csv')


# Select the columns you want to plot
# Replace 'column1' and 'column2' with the actual column names
column = "F1 score"
column1 = df1[column]
column2 = df2[column]
column3 = df3[column]

# Create a figure and a set of subplots
fig, ax = plt.subplots()

# Create boxplots
ax.boxplot([column1, column2, column3])

# Set x-axis labels
ax.set_xticklabels(['Cell-Division', 'Mir-9-neurogeneses', 'Tumor cell invasion\n and migration'])

# Set the title
ax.set_title(f'{column} - 30 runs')
ax.margins(y=0.5)
ax.set_ylim([0, 100])

# Calculate metrics for each column
metrics1 = {'mean': column1.mean(), 'median': column1.median()}
metrics2 = {'mean': column2.mean(), 'median': column2.median()}

# Display metrics on the plot
# ax.text(1, max(column1), f"Mean: {metrics1['mean']:.2f}\nMedian: {metrics1['median']:.2f}", ha='center')
# ax.text(2, max(column2), f"Mean: {metrics2['mean']:.2f}\nMedian: {metrics2['median']:.2f}", ha='center')

# Show the plot
plt.show()