# import pandas as pd
# # ==========================================
# # E-Commerce Dataset Cleaning & Merging
# # ==========================================

# import pandas as pd

# # -----------------------------
# # Step 1: Load datasets
# # -----------------------------
# basket_df = pd.read_csv("basket_details.csv")
# customer_df = pd.read_csv("customer_details.csv")

# # -----------------------------
# # Step 2: Display basic info
# # -----------------------------
# print("Basket Dataset Shape:", basket_df.shape)
# print("Customer Dataset Shape:", customer_df.shape)

# # -----------------------------
# # Step 3: Merge datasets
# # Common column = customer_id
# # -----------------------------
# merged_df = pd.merge(
#     basket_df,
#     customer_df,
#     on="customer_id",
#     how="inner"      # keeps only matching customer IDs
# )

# print("\nMerged Dataset Shape:", merged_df.shape)

# # -----------------------------
# # Step 4: Check Missing Values
# # -----------------------------
# print("\nMissing Values Before Cleaning:")
# print(merged_df.isnull().sum())

# # -----------------------------
# # Step 5: Handle Missing Values
# # -----------------------------
# # Numeric columns -> fill with median
# numeric_cols = merged_df.select_dtypes(include=["number"]).columns

# for col in numeric_cols:
#     merged_df[col] = merged_df[col].fillna(merged_df[col].median())

# # Categorical columns -> fill with mode
# categorical_cols = merged_df.select_dtypes(include=["object"]).columns

# for col in categorical_cols:
#     merged_df[col] = merged_df[col].fillna(merged_df[col].mode()[0])

# # -----------------------------
# # Step 6: Remove Duplicate Rows
# # -----------------------------
# duplicates_before = merged_df.duplicated().sum()
# print("\nDuplicate Rows Found:", duplicates_before)

# merged_df = merged_df.drop_duplicates()

# duplicates_after = merged_df.duplicated().sum()
# print("Duplicate Rows After Cleaning:", duplicates_after)

# # -----------------------------
# # Step 7: Verify Missing Values
# # -----------------------------
# print("\nMissing Values After Cleaning:")
# print(merged_df.isnull().sum())

# # -----------------------------
# # Step 8: Save Clean Dataset
# # -----------------------------
# output_file = "final_ecommerce_clean.csv"

# merged_df.to_csv(output_file, index=False)

# print(f"\nClean dataset saved successfully as '{output_file}'")

# # -----------------------------
# # Step 9: Preview Final Dataset
# # -----------------------------
# print("\nFirst 5 Rows:")
# print(merged_df.head())
# # ==========================================
# # Top 5 Most Frequent Products using Seaborn
# # ==========================================

# ==========================================
# Customer Distribution by Age Group
# ==========================================

# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt

# # Load Clean Dataset
# df = pd.read_csv("final_ecommerce_clean.csv")

# # Create Age Groups
# df["age_group"] = pd.cut(
#     df["customer_age"],
#     bins=[0, 20, 30, 40, 50, 60, 100],
#     labels=["0-20", "21-30", "31-40", "41-50", "51-60", "60+"]
# )

# # Count Customers in Each Age Group
# age_counts = (
#     df["age_group"]
#     .value_counts()
#     .sort_index()
#     .reset_index()
# )

# age_counts.columns = ["Age Group", "Number of Customers"]

# # Set Plot Style
# sns.set_style("whitegrid")

# # Create Bar Plot
# plt.figure(figsize=(8, 5))

# ax = sns.barplot(
#     data=age_counts,
#     x="Age Group",
#     y="Number of Customers"
# )

# # Add Values on Top of Bars
# for p in ax.patches:
#     ax.annotate(
#         str(int(p.get_height())),
#         (p.get_x() + p.get_width()/2, p.get_height()),
#         ha='center',
#         va='bottom'
#     )

# # Labels and Title
# plt.title("Customer Distribution by Age Group", fontsize=14)
# plt.xlabel("Age Group")
# plt.ylabel("Number of Customers")

# plt.tight_layout()

# # Save Graph
# plt.savefig("customer_age_distribution.png", dpi=300)

# # Show Graph
# plt.show()

# print("Graph saved as 'customer_age_distribution.png'")
# ==========================================
# E-Commerce Data Analysis (All Graphs)
# ==========================================

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load Dataset
df = pd.read_csv("final_ecommerce_clean.csv")

# Style
sns.set_style("whitegrid")

# ==========================================
# Graph 1: Male vs Female Customers
# ==========================================
plt.figure(figsize=(6,4))
sns.countplot(data=df, x="sex")
plt.title("Male vs Female Customers")
plt.xlabel("Gender")
plt.ylabel("Number of Customers")
plt.tight_layout()
plt.savefig("gender_distribution.png", dpi=300)
plt.show()

# ==========================================
# Graph 2: Customer Age Distribution
# ==========================================
plt.figure(figsize=(8,5))
sns.histplot(df["customer_age"], bins=10, kde=True)
plt.title("Customer Age Distribution")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("age_distribution.png", dpi=300)
plt.show()

# ==========================================
# Graph 3: Total Basket Count by Gender
# ==========================================
gender_sales = (
    df.groupby("sex")["basket_count"]
      .sum()
      .reset_index()
)

plt.figure(figsize=(6,4))
sns.barplot(
    data=gender_sales,
    x="sex",
    y="basket_count"
)

plt.title("Total Basket Count by Gender")
plt.xlabel("Gender")
plt.ylabel("Total Basket Count")
plt.tight_layout()
plt.savefig("basket_by_gender.png", dpi=300)
plt.show()

# ==========================================
# Graph 4: Top 10 Products by Basket Count
# ==========================================
top_products = (
    df.groupby("product_id")["basket_count"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

plt.figure(figsize=(10,5))
sns.barplot(
    x=top_products.index.astype(str),
    y=top_products.values
)

plt.title("Top 10 Products by Basket Count")
plt.xlabel("Product ID")
plt.ylabel("Total Basket Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("top_products.png", dpi=300)
plt.show()

# ==========================================
# Graph 5: Customer Tenure Distribution
# ==========================================
plt.figure(figsize=(8,5))
sns.histplot(df["tenure"], bins=10, kde=True)

plt.title("Customer Tenure Distribution")
plt.xlabel("Tenure")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("tenure_distribution.png", dpi=300)
plt.show()

# ==========================================
# Graph 6: Monthly Basket Trend
# ==========================================
df["basket_date"] = pd.to_datetime(df["basket_date"])

monthly_sales = (
    df.groupby(df["basket_date"].dt.to_period("M"))
      ["basket_count"]
      .sum()
)

monthly_sales.index = monthly_sales.index.astype(str)

plt.figure(figsize=(10,5))
sns.lineplot(
    x=monthly_sales.index,
    y=monthly_sales.values,
    marker="o"
)

plt.title("Monthly Basket Trend")
plt.xlabel("Month")
plt.ylabel("Total Basket Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("monthly_trend.png", dpi=300)
plt.show()

# ==========================================
# Summary Statistics
# ==========================================
print("\nDataset Shape:", df.shape)

print("\nGender Distribution:")
print(df["sex"].value_counts())

print("\nTop 10 Products:")
print(top_products)

print("\nCustomer Age Statistics:")
print(df["customer_age"].describe())

print("\nCustomer Tenure Statistics:")
print(df["tenure"].describe())

print("\nAll graphs generated and saved successfully!")