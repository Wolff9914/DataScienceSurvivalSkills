import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

dataset = pd.read_csv("census_income_dataset.csv")

'''
Plot 1: Age distribution of respondents
'''
# Copy dataset
data_age = dataset.copy()
# Remove missing values
data_age = data_age[~data_age["AGE"].isnull()] 

# Amount of age values
age_counts = data_age["AGE"].value_counts().sort_index()  # Sort by age

# Scatterplot erstellen
sns.scatterplot(x=age_counts.index, y=age_counts.values, color='blue')
sns.lineplot(x=age_counts.index, y=age_counts.values, color='blue', linestyle='-')

# Achsen und Titel hinzufügen
plt.xlabel('Age')
plt.ylabel('Number of Respondents')
plt.title('Age distribution of respondents')
plt.savefig("plots/data_age.svg")
plt.show()


'''
Plot 2: How often does each relationship status occur?
'''
# Copy dataset
data_relation = dataset.copy()
# Remove missing values
data_relation = data_relation[~data_relation["RELATIONSHIP"].isnull()] 

sns.countplot(data=data_relation, x="RELATIONSHIP", width=0.5)

plt.ylabel('Number of Respondents')
plt.xlabel('')
plt.xticks(rotation=45, ha="right")
plt.title('Relationship status distribution of respondents')
plt.savefig("plots/data_relation.svg")
plt.show()


'''
Plot 3: How many respondents have a salary of <=50k or >50k within each educational level
'''

data_salary = dataset.copy()

data_salary = data_salary[~data_salary["EDUCATION"].isnull()]
data_salary = data_salary[~data_salary["SALARY"].isnull()]

# Gehaltskategorien zu numerischen Werten konvertieren
data_salary["SALARY"] = data_salary["SALARY"].str.strip()
# Bildungsniveau anhand von EDUCATION-NUM sortieren
education_order = (
    data_salary.groupby("EDUCATION")["EDUCATION-NUM"].mean().sort_values().index
)

# Gruppieren der Daten
grouped_data = data_salary.groupby(["EDUCATION", "SALARY"]).size().reset_index(name="count")
print(grouped_data)
# Barplot mit sortierten Kategorien erstellen
sns.barplot(data=grouped_data, y="EDUCATION", x="count", hue="SALARY", palette="viridis", order=education_order)

# Plot-Titel und Achsentitel
plt.xlabel("Number of Respondents")
plt.ylabel("")
plt.title("Salary Distribution by Educational Level")
plt.legend()
plt.savefig("plots/data_salary.svg")
plt.show()
