# Import the required libraries
import os
import io
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt

# Ensure 'static' directory exists
if not os.path.exists("static"):
    os.makedirs("static")

# Load the dataset
df_churn = pd.read_csv("Telecom-Customer-Churn.csv")

# Save the first few rows as a CSV
df_churn.head().to_csv("static/churn_head.csv", index=False)

# Get the shape of the dataframe
df_shape = df_churn.shape

# Save the shape as a text file (or send it via API)
with open("static/dataset_shape.txt", "w") as f:
    f.write(f"Rows: {df_shape[0]}, Columns: {df_shape[1]}")

# Get the columns of the dataframe
columns = df_churn.columns.values

# Save the columns as a text file
with open("static/columns.txt", "w") as f:
    f.write(", ".join(columns))  # Join the column names as a comma-separated string

# Get the data types of the columns
dtypes = df_churn.dtypes

# Save the data types as a text file
with open("static/dtypes.txt", "w") as f:
    for column, dtype in dtypes.items():
        f.write(f"{column}: {dtype}\n")  # Save each column with its dtype

# Get the descriptive statistics of numeric columns
describe_stats = df_churn.describe()

# Save the descriptive statistics to a text file
with open("static/describe_stats.txt", "w") as f:
    f.write(describe_stats.to_string())  # Save the describe output as a string

# Plot the count of the target variable 'Churn'
churn_counts = df_churn['Churn'].value_counts()

# Create a horizontal bar plot
plt.figure(figsize=(8, 6))
churn_counts.plot(kind='barh')
plt.xlabel("Count", labelpad=14)
plt.ylabel("Target Variable", labelpad=14)
plt.title("Count of TARGET Variable per category", y=1.02)

# Save the plot as an image
plt.savefig("static/churn_counts.png")
plt.close()  # Close the plot to avoid it being displayed in the backend

# Calculate the percentage distribution of the 'Churn' column
churn_percentage = 100 * df_churn['Churn'].value_counts() / len(df_churn['Churn'])

# Save the percentage distribution as a text file
with open("static/churn_percentage.txt", "w") as f:
    f.write(churn_percentage.to_string())  # Save the result as a string

# Get the value counts of the 'Churn' column
churn_value_counts = df_churn['Churn'].value_counts()

# Save the value counts as a text file
with open("static/churn_value_counts.txt", "w") as f:
    f.write(churn_value_counts.to_string())  # Save value counts as a string

# Capture the output of df.info(verbose=True)
buffer = io.StringIO()
df_churn.info(verbose=True, buf=buffer)
df_info_summary = buffer.getvalue()

# Save the summary to a text file
with open("static/churn_info.txt", "w") as f:
    f.write(df_info_summary)

# Calculate the percentage of missing values for each column
missing_values = (df_churn.isnull().sum() * 100 / df_churn.shape[0])

# Save the missing values percentage as a text file
with open("static/missing_values.txt", "w") as f:
    f.write(missing_values.to_string())  # Save the result as a string

# Generate and save the missing values plot
plt.figure(figsize=(16, 5))
ax = sns.pointplot(x=missing_values.index, y=missing_values.values)
plt.xticks(rotation=90, fontsize=7)
plt.title("Percentage of Missing Values")
plt.ylabel("PERCENTAGE")
plt.xlabel("Columns")
plt.savefig("static/missing_values_plot.png", bbox_inches='tight')  # Save as image
plt.close()

# Create a copy of the dataset
telco_data = df_churn.copy()

# Convert 'TotalCharges' to numeric, setting errors='coerce' to handle non-numeric values
telco_data['TotalCharges'] = pd.to_numeric(telco_data['TotalCharges'], errors='coerce')

# Drop rows with missing values
telco_data.dropna(how='any', inplace=True)

# If you prefer filling missing values with 0 instead of dropping:
# telco_data.fillna(0, inplace=True)

# Now, use telco_data for all further analysis
df_churn = telco_data  # Replace the original dataset reference

# Group the tenure into bins of 12 months
labels = ["{0} - {1}".format(i, i + 11) for i in range(1, 72, 12)]

# Create a new column 'tenure_group' with the binned values
telco_data['tenure_group'] = pd.cut(telco_data['tenure'], range(1, 80, 12), right=False, labels=labels)

# The 'tenure_group' column is now added to 'telco_data' but won't be shown on the frontend

# Calculate the value counts of tenure groups
tenure_group_counts = telco_data['tenure_group'].value_counts()

# Save the tenure group counts as a string
with open("static/tenure_group_counts.txt", "w") as f:
    f.write(tenure_group_counts.to_string())  # Save value counts as a string

# Drop 'customerID' and 'tenure' columns from the DataFrame
telco_data.drop(columns=['customerID'], axis=1, inplace=True)

# Optionally, you can save the head of the data (for reference if needed)
telco_data.head().to_csv("static/modified_data_head.csv", index=False)

# Loop through each predictor (except 'Churn', 'TotalCharges', 'MonthlyCharges')
for i, predictor in enumerate(telco_data.drop(columns=['Churn', 'TotalCharges', 'MonthlyCharges'])):
    plt.figure(i)
    sns.countplot(data=telco_data, x=predictor, hue='Churn')

    # Save the plot as an image
    plt.savefig(f"static/{predictor}_countplot.png")
    plt.close()  # Close the figure to avoid memory issues

# Convert 'Churn' column to binary (1 for 'Yes', 0 for 'No')
telco_data['Churn'] = np.where(telco_data.Churn == 'Yes', 1, 0)

# Convert categorical variables into dummy/one-hot encoded variables
telco_data_dummies = pd.get_dummies(telco_data)

# Scatter plot of MonthlyCharges vs TotalCharges
plt.figure(figsize=(8,6))
sns.lmplot(data=telco_data_dummies, x='MonthlyCharges', y='TotalCharges', fit_reg=False)

# Save the plot
plt.savefig("static/monthly_vs_total_charges.png")
plt.close()

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os

# Create a function to generate the KDE plot
def generate_monthly_charges_kde():
        # Create the figure for the plot
        plt.figure(figsize=(10, 6))

        # Generate the KDE plot for customers who did not churn (Churn == 0)
        Mth = sns.kdeplot(telco_data_dummies.MonthlyCharges[telco_data_dummies["Churn"] == 0],
                          color="Red", shade=True)
        
        # Generate the KDE plot for customers who churned (Churn == 1)
        Mth = sns.kdeplot(telco_data_dummies.MonthlyCharges[telco_data_dummies["Churn"] == 1],
                          ax=Mth, color="Blue", shade=True)

        # Set the legend, labels, and title
        Mth.legend(["No Churn", "Churn"], loc='upper right')
        Mth.set_ylabel('Density')
        Mth.set_xlabel('Monthly Charges')
        Mth.set_title('Monthly Charges by Churn')

        # Create a path for saving the plot in the static directory
        save_path = os.path.join('static', 'monthly_charges_kde.png')
        
        # Save the plot as a PNG image
        plt.savefig(save_path, bbox_inches='tight')
        plt.close()  # Close the plot to free memory

# Call the function to generate and save the plot
generate_monthly_charges_kde()

# Generate and save the Total Charges KDE plot
def save_total_charges_kde():
    Tot = sns.kdeplot(telco_data_dummies.TotalCharges[(telco_data_dummies["Churn"] == 0)],
                      color="Red", shade=True)
    Tot = sns.kdeplot(telco_data_dummies.TotalCharges[(telco_data_dummies["Churn"] == 1)],
                      ax=Tot, color="Blue", shade=True)
    Tot.legend(["No Churn", "Churn"], loc='upper right')
    Tot.set_ylabel('Density')
    Tot.set_xlabel('Total Charges')
    Tot.set_title('Total charges by churn')

    # Save as an image
    plt.savefig("static/total_charges_kde.png", bbox_inches='tight')
    plt.close()

save_total_charges_kde()

# Generate and save the Churn correlation bar plot
def save_churn_correlation_plot():
    plt.figure(figsize=(20, 8))
    telco_data_dummies.corr()['Churn'].sort_values(ascending=False).plot(kind='bar')

    # Save the plot as an image
    plt.savefig("static/churn_correlation_bar.png", bbox_inches='tight')
    plt.close()

save_churn_correlation_plot()

# Generate and save the heatmap of the correlation matrix
plt.figure(figsize=(12, 12))
sns.heatmap(telco_data_dummies.corr(), cmap="Paired")

# Save the plot as an image
plt.savefig("static/correlation_heatmap.png", bbox_inches='tight')
plt.close()

# Assuming telco_data is already loaded in the code
new_df1_target0 = telco_data.loc[telco_data["Churn"] == 0]
new_df1_target1 = telco_data.loc[telco_data["Churn"] == 1]

# Function to Plot
def uniplot(df, col, title, hue=None):
    sns.set_style('whitegrid')
    sns.set_context('talk')
    plt.rcParams["axes.labelsize"] = 20
    plt.rcParams['axes.titlesize'] = 22
    plt.rcParams['axes.titlepad'] = 30

    # Set fixed figure size
    fig, ax = plt.subplots(figsize=(12, 6))  # Fixed size for better visibility

    plt.xticks(rotation=45)
    plt.title(title)

    # Plot countplot
    sns.countplot(data=df, x=col, order=df[col].value_counts().index, hue=hue, palette='bright')

    # Save each plot with a dynamic name based on the title or column
    save_path = f"static/{title.replace(' ', '_').replace('/', '_')}.png"  # Replace spaces and slashes to prevent path issues
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()

uniplot(new_df1_target1, col='Partner', title='Distribution of Gender for Churned Customers', hue='gender')
uniplot(new_df1_target0, col='Partner', title='Distribution of Gender for Non Churned Customers', hue='gender')
uniplot(new_df1_target1, col='PaymentMethod', title='Distribution of PaymentMethod for Churned Customers', hue='gender')
uniplot(new_df1_target1, col='Contract', title='Distribution of Contract for Churned Customers', hue='gender')
uniplot(new_df1_target1, col='TechSupport', title='Distribution of TechSupport for Churned Customers', hue='gender')
uniplot(new_df1_target1, col='SeniorCitizen', title='Distribution of SeniorCitizen for Churned Customers', hue='gender')

# Example DataFrame df_churn (replace with your actual DataFrame)
num_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
for col in num_cols:
    plt.figure(figsize=(8, 4))
    sns.histplot(df_churn, x=col, hue="Churn", kde=True, bins=30, palette="viridis", alpha=0.7)
    plt.title(f'Distribution of {col} by Churn Status')
    plt.savefig(f"static/distribution_{col}_by_churn.png", bbox_inches='tight')  # Save the plot as an image
    plt.close()

# Create the box plot for 'Customer Segmentation by Contract Type and Tenure'
plt.figure(figsize=(10, 5))
sns.boxplot(data=df_churn, x="Contract", y="tenure", hue="Churn", palette="magma")
plt.title("Customer Segmentation by Contract Type and Tenure")
plt.savefig("static/customer_segmentation_by_contract_tenure.png", bbox_inches='tight')
plt.close()

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# Encoding categorical features
df_encoded = df_churn.copy()

# Drop the 'tenure_group' column if it exists
if 'tenure_group' in df_encoded.columns:
    df_encoded = df_encoded.drop(columns=['tenure_group'])

for col in df_encoded.select_dtypes(include=['object']).columns:
    df_encoded[col] = LabelEncoder().fit_transform(df_encoded[col])

# Splitting data
X = df_encoded.drop(columns=['Churn'])
y = df_encoded['Churn']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Plot feature importance
feat_importances = pd.Series(rf.feature_importances_, index=X.columns)
feat_importances.nlargest(10).plot(kind='barh', colormap="viridis")
plt.title("Top 10 Feature Importances (Random Forest)")
plt.savefig("static/feature_importance_random_forest.png", bbox_inches='tight')
plt.close()

from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt

# Perform K-Means clustering
kmeans = KMeans(n_clusters=3, random_state=42)
df_encoded['Cluster'] = kmeans.fit_predict(X)

# Plot the clusters
plt.figure(figsize=(10, 5))
sns.scatterplot(x=df_encoded['tenure'], y=df_encoded['MonthlyCharges'], hue=df_encoded['Cluster'], palette="viridis")
plt.title("Customer Clusters based on Tenure and Monthly Charges")
plt.savefig("static/customer_clusters_tenure_monthlycharges.png", bbox_inches='tight')
plt.close()