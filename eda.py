import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("phishing_url_dataset.csv")  # Replace with your dataset file path

# Display basic information about the dataset
print("Dataset Overview")
print(df.info())
print("\nFirst 5 Rows:")
print(df.head())

# Check for missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Summary statistics for numerical columns
print("\nSummary Statistics:")
print(df.describe())

# Unique counts for categorical columns
print("\nUnique Values in Categorical Columns:")
for col in df.select_dtypes(include='object').columns:
    print(f"{col}: {df[col].nunique()} unique values")

# Check the distribution of the target variable (if present)
if "type" in df.columns:  # Replace "type" with the actual target column name
    print("\nTarget Variable Distribution:")
    print(df["type"].value_counts())
    sns.countplot(x="type", data=df)
    plt.title("Target Variable Distribution")
    plt.show()

# Correlation heatmap for numerical features
numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
if len(numerical_cols) > 1:
    plt.figure(figsize=(10, 8))
    sns.heatmap(df[numerical_cols].corr(), annot=True, cmap='coolwarm')
    plt.title("Correlation Heatmap")
    plt.show()

# Plot distribution of numerical features
for col in numerical_cols:
    plt.figure(figsize=(8, 6))
    sns.histplot(df[col], kde=True)
    plt.title(f"Distribution of {col}")
    plt.show()

# Analyze URL-related features (e.g., length of URLs)
if "URL" in df.columns:  # Replace "URL" with the column containing URLs
    df["url_length"] = df["URL"].apply(len)
    print("\nURL Length Statistics:")
    print(df["url_length"].describe())
    plt.figure(figsize=(8, 6))
    sns.histplot(df["url_length"], kde=True)
    plt.title("Distribution of URL Length")
    plt.show()
