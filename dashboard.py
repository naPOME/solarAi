import pandas as pd



df1 = pd.read_csv('/home/pom/solar/data/sierraleone-bumbuna.csv')
df2 = pd.read_csv('/home/pom/solar/data/benin-malanville.csv')
df3 = pd.read_csv('/home/pom/solar/data/togo-dapaong_qc.csv')


print(df1.head())
print(df2.head())
print(df3.head())
