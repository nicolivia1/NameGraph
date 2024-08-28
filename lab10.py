# Author: Nicole Sausville
# Assignment: Lab 10
# Due Date: 8/23/2024
# Description: A program that graphs the popularity of male babies
# named Aiden vs. Ayden over a year-by-year basis and displays
# the percentage of the name Aiden over the total.
# Sources: tutoring

import pandas as pd
import pyodbc
import matplotlib.pyplot as plt

# Connects to the database
name_connection = pyodbc.connect(
    server='cisdbss.pcc.edu',
    database='NAMES',
    user='275student',
    password='275student',
    driver='{ODBC Driver 18 for SQL Server}' + ";TrustServerCertificate=yes"
)

sql = """
SELECT Year, Name, Gender, NameCount
FROM all_data
WHERE Gender = 'M' AND Name = 'Aiden'
OR Gender = 'M' AND Name = 'Ayden';

"""

# Preparing the data
long_data = pd.read_sql(sql, name_connection)

wide_data = long_data.pivot(index="Year", columns="Name", values="NameCount")
wide_data = wide_data.reset_index()
wide_data.columns.name = None

# Fill all the NaN values with 0's
wide_data = wide_data.fillna(0)

# Plotting the data
plt.figure(figsize=(12, 8), dpi=72)
plt.plot('Year', 'Aiden', data=wide_data)
plt.plot('Year', 'Ayden', data=wide_data)

# Adding Graph descriptions
plt.grid()
plt.title("Popularity of Aiden vs Ayden")
plt.xlabel("Year")
plt.ylabel("Number of Babies")
plt.legend(['Aiden', 'Ayden'])
plt.show()

# Calculating percentage column
wide_data['Percent of Aiden'] = 100 * wide_data['Aiden'] / (wide_data['Aiden'] + wide_data['Ayden'])

# Graphing the percentage
plt.figure(figsize=(12, 8), dpi=72)
plt.plot('Year', "Percent of Aiden", data=wide_data)

# Adding graph details
plt.grid()
plt.title("Is Aiden or Ayden More Popular")
plt.xlabel("Year")
plt.ylabel("Percent of Babies Named Aiden")

# Shows the graph
plt.show()

print(wide_data.to_string())