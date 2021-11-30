import pandas as pd

a = pd.read_csv("2019.csv")
b = pd.read_csv("country-codes.csv")
# b = b.dropna(axis=1)
merged = a.merge(b, left_on='Country or region',
                 right_on='English short name lower case')
merged = merged.drop(['English short name lower case', 'Alpha-2 code',
                      'Numeric code', 'ISO 3166-2'], axis=1)
merged.to_csv("whr2019.csv", index=False)
