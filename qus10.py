
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("marks.csv")

print(df)

df["Marks"] = pd.to_numeric(df["Marks"], errors="coerce")
df = df.dropna(subset=["Marks"])

print("\nAverage Marks:", round(df["Marks"].mean(), 2))
print("Highest Marks:", df["Marks"].max())
print("Lowest Marks:", df["Marks"].min())

plt.bar(df["Name"], df["Marks"])
plt.xlabel("Student Name")
plt.ylabel("Marks")
plt.title("Student Marks Dashboard")
plt.tight_layout()
plt.show()
