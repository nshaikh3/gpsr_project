import numpy
import pandas as pd

myfile = pd.ExcelFile(r'C:\Users\noor-\Desktop\Waterloo\Research\GeoPolRisk.xlsx')

print(myfile.sheet_names)

countries = myfile.parse('Countries')
countries = countries.set_index('Country Code')
countries.head(10)

materials = myfile.parse('Commodity')
materials = materials.drop("Notes", axis=1)
materials = materials.set_index('HS Code')
materials.head(10)


wgi = myfile.parse('WGI Scores')
wgi = wgi.set_index(['Year', 'Country Code'])
wgi.head(10)

prodata = myfile.parse('usgs 2015')
prodata = prodata.iloc[:, :-1]
prodata = prodata.drop('Commodity', axis=1)
prodata = prodata.set_index(['Year', 'HS Code'])
prodata = prodata.fillna(0.0)
prodata = prodata.replace("No data", 0.0).astype('float64', errors='ignore')
prodata['USA'] = pd.to_numeric(prodata['USA'])
prodata.index.levels[-1].astype('float64')
prodata.head(50)

hhi = prodata.divide(prodata.iloc[:, -1], axis='rows').pow(2)
hhi = hhi.iloc[:, :-1]
hhi.head(10)
hhifinal = hhi.sum(axis=1).subtract(hhi.loc[:, "Canada"]).subtract(
      hhi.loc[:, "USA"]).subtract(hhi.loc[:, "Austria"]).subtract(
            hhi.loc[:, "Belgium"]).subtract(hhi.loc[:, "Bulgaria"]).subtract(
                  hhi.loc[:, "Cyprus"]).subtract(hhi.loc[:, "Denmark"]).subtract(
                         hhi.loc[:, "Estonia"]).subtract(hhi.loc[:, "Finland"]).subtract(
                               hhi.loc[:, "France"]).subtract(hhi.loc[:, "Germany"]).subtract(
                                     hhi.loc[:, "Greece"]).subtract(hhi.loc[:, "Hungary"]).subtract(
                                           hhi.loc[:, "Ireland"]).subtract(hhi.loc[:, "Italy"]).subtract(
                                                 hhi.loc[:, "Latvia"]).subtract(hhi.loc[:, "Lithuania"]).subtract(
                                                       hhi.loc[:, "Netherlands"]).subtract(hhi.loc[:, "Poland"]).subtract(
                                                             hhi.loc[:, "Portugal"]).subtract(hhi.loc[:, "Romania"]).subtract(
                                                                   hhi.loc[:, "Slovakia"]).subtract(hhi.loc[:, "Slovenia"]).subtract(
                                                                         hhi.loc[:, "Sweden"]).subtract(hhi.loc[:, "Spain"]).subtract(
                                                                               hhi.loc[:, "UK"]).subtract(hhi.loc[:, "Czech Republic"]
                  )

# hhi[eu_countries]

hhifinal.index.levels[-1].astype('float64')
hhifinal.head(10)

trade = myfile.parse('trade')
trade = trade.set_index(['Year', 'HS Code', 'Country Code'])
trade = trade.fillna(0.0)
trade.index.levels[-1].astype('float64')
trade.head(10)