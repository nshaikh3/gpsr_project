import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

myfile2 = pd.ExcelFile(r'C:\Users\noor-\Desktop\Waterloo\Research\GeoPolRisk.xlsx')
print(myfile2.sheet_names)

countries = myfile2.parse('Countries')
countries = countries.set_index('Country Code')
#countries.head(10)

# Used for the materials table
materials = myfile2.parse('Commodity')
materials = materials.drop("Notes", axis=1)
materials = materials.set_index('HS Code')
#materials.head(10)

# Used to get the WGI table
wgi = myfile2.parse('WGI Scores')
wgi = wgi.set_index(['Year', 'Country Code'])
#wgi.index = wgi.index.astype('float64')
#wgi.head(10)

prodata = myfile2.parse('usgs 2015')
#prodata = prodata.iloc[:, :-1]
prodata = prodata.drop('Commodity', axis=1)
prodata = prodata.set_index(['Year', 'HS Code'])
prodata = prodata.fillna(0.0)
prodata = prodata.replace("No data", 0.0).astype('float64', errors='ignore')
#prodata['USA'] = pd.to_numeric(prodata['USA'])
prodata.index.levels[-1].astype('float64')
#prodata.index = prodata.index.astype('float64')
#prodata.head(10)

worldprodata = prodata.iloc[:, -1]

hhi = prodata.div(worldprodata, axis='rows').pow(2)
hhi = hhi.iloc[:, :-1]
#hhi.head(-10)

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
#hhifinal.head(100)

trade = myfile2.parse('trade')
trade = trade.set_index(['Year', 'HS Code', 'Country Code'])
trade = trade.fillna(0.0)
trade.index.levels[-1].astype('float64')
#trade.head(100)

def wgi_score(country, year):
    print("WGI Score: {}".format(wgi.loc[(year, country), 'WGI Score']))

def hhicalc(material, year):
    return hhifinal.loc[(year, material)]

def gpol(year, country, material, indicator):
    
      country_name = countries.loc[country, 'Country Name']
      print("Country Name: {}".format(country_name))
    
      material_name = materials.loc[material, 'Commodity']
      print("Commodity: {}".format(material_name))

      indicator_table = wgi.loc[:, ("Country Name", indicator)]
    
      trade_denom = prodata.loc[(year, material),
                              country_name]+trade.loc[(year, material, 
                                                      country), 0].values
      t = trade.loc[(year, material, country), :]
      t = t.iloc[0, :]
      t = t[t!=0].rename("Amount")
      t.index.name = "Country Code"
    
      indicator_year = indicator_table.loc[year, :]
      t = pd.concat((indicator_year, t), axis=1)
      t = t.dropna(subset=['Amount', indicator])
      if 839 in t.index:
            totsupply = trade.loc[(year, material, country), 0]
            weightedsupply = t.loc[:, "WGI Score"].mul(t.loc[:, "Amount"].reindex())
            weightedsupply = weightedsupply /(totsupply.values)
            updatedwgi = weightedsupply.sum()
            t.at[839, indicator] = updatedwgi
        
      adj_trade = t.loc[:, "Amount"].apply(lambda x: x/trade_denom, 0).reindex()
    
      fin_trade = adj_trade.apply(lambda x: x*t.loc[:, indicator])
      weight_sum = fin_trade.sum(axis=0)

      geopol = weight_sum*hhifinal.loc[year, material]
      #print("The GeoPolitical Supply Risk for {} is {}".format(country_name, geopol.loc[(year, material)]))
    
      return geopol.loc[(year, material)]

def rec_red(year, country, material, reduction, indicator):

      country_name = countries.loc[country, 'Country Name']
      indicator_table = wgi.loc[:, ("Country Name", indicator)]
    # used to create new table for bcs and wcs
      b = trade.loc[(year, material, country), :]
      b = b.iloc[0, :]
      b = b[b!=0].rename("Amount")
      b.index.name = "Country Code"
    
      indicator_year = indicator_table.loc[year, :]
      b = pd.concat((indicator_year, b), axis=1)
      b = b.dropna(subset=['Amount', indicator])

      if 839 in b.index:
            totsupply = trade.loc[(year, material, country), 0]
            weightedsupply = b.loc[:, "WGI Score"].mul(b.loc[:, "Amount"].reindex())
            weightedsupply = weightedsupply /(totsupply.values)
            updatedwgi = weightedsupply.sum()
            b.at[839, indicator] = updatedwgi
        
      bcs = b.sort_values((indicator), ascending=False).reindex()
      bcs.index.name = 'Country Code'    
    
      wcs = b.sort_values((indicator), ascending=True).reindex()
      wcs.index.name = 'Country Code'
        
      a = (trade.loc[(year, material, country), 0]).values*(reduction*0.01)

# Best case scenario

      for row in bcs.itertuples():
            if bcs.at[row.Index, "Amount"] - a < 0:
                  bcs.at[row.Index, "New Amount"] = 0
                  bcs.at[row.Index, "New Amount2"] = a
        
            else:
                  bcs.at[row.Index, "New Amount"] = bcs.at[row.Index, "Amount"] - a
                  bcs.at[row.Index, "New Amount2"] = a
    
            a = a - bcs.at[row.Index, "Amount"]
        
      for row in bcs.itertuples():
            if bcs.at[row.Index, "New Amount2"] < 0:
                  bcs.at[row.Index, "New Amount"] = bcs.at[row.Index, "Amount"]
            
            
      trade_denom_bcs = prodata.loc[(year, material), country_name] + trade.loc[(year, material, country), 0].values
    
      adj_trade2 = bcs.loc[:, "New Amount"].apply(lambda x: x/trade_denom_bcs, 0).reindex()

      fin_trade2 = adj_trade2.apply(lambda x: x*bcs.loc[:, indicator])
      weight_sum = fin_trade2.sum()
      geopol_bcs = weight_sum*hhifinal.loc[year, material]
    
    #print("Updated GPSR for best-case scenario: {}".format(geopol_bcs.loc[(year, material)]))
    #print(geopol_bcs.loc[(year, material)])

# Worst case scenario
      a2 = (trade.loc[(year, material, country), 0]).values*(reduction*0.01)
    
      for row in wcs.itertuples():
            if wcs.at[row.Index, "Amount"] - a2 < 0:
                  wcs.at[row.Index, "New Amount"] = 0
                  wcs.at[row.Index, "New Amount2"] = a2
        
            else:
                  wcs.at[row.Index, "New Amount"] = wcs.at[row.Index, "Amount"] - a2
                  wcs.at[row.Index, "New Amount2"] = a2
    
            a2 = a2 - wcs.at[row.Index, "Amount"]
        
      for row in wcs.itertuples():
            if wcs.at[row.Index, "New Amount2"] < 0:
                  wcs.at[row.Index, "New Amount"] = wcs.at[row.Index, "Amount"]
            
      trade_denom_wcs = prodata.loc[(year, material), country_name] + trade.loc[(year, material, country), 0].values
    
      adj_trade3 = wcs.loc[:, "New Amount"].apply(lambda x: x/trade_denom_wcs, 0).reindex()

      fin_trade3 = adj_trade3.apply(lambda x: x*wcs.loc[:, indicator])
      weight_sum2 = fin_trade3.sum()
      geopol_wcs = weight_sum2*hhifinal.loc[year, material]
    
    #print("Updated GPSR for worst-case scenario: {}".format(geopol_wcs.loc[(year, material)]))
    #print(geopol_wcs.loc[(year, material)])
   
      #print("The GPSR ranges from {} - {} after accounting for the recycling reduction of {}%".
          #format(geopol_bcs.loc[(year, material)], geopol_wcs.loc[(year, material)], reduction))
        
      return (geopol_bcs.loc[(year, material)], geopol_wcs.loc[(year, material)])

def rec_red_plot(year, country, material):
      y0 = rec_red(year, country, material, 0, "WGI Score")
      y5 = rec_red(year, country, material, 5, "WGI Score")
      y10 = rec_red(year, country, material, 10, "WGI Score")
      y15 = rec_red(year, country, material, 15, "WGI Score")
      y20 = rec_red(year, country, material, 20, "WGI Score")
      y25 = rec_red(year, country, material, 25, "WGI Score")
      y30 = rec_red(year, country, material, 30, "WGI Score")
      y35 = rec_red(year, country, material, 35, "WGI Score")
      y40 = rec_red(year, country, material, 40, "WGI Score")
      y45 = rec_red(year, country, material, 45, "WGI Score")
      y50 = rec_red(year, country, material, 50, "WGI Score")
      y55 = rec_red(year, country, material, 55, "WGI Score")
      y60 = rec_red(year, country, material, 60, "WGI Score")
      y65 = rec_red(year, country, material, 65, "WGI Score")
      y70 = rec_red(year, country, material, 70, "WGI Score")
      y75 = rec_red(year, country, material, 75, "WGI Score")
      y80 = rec_red(year, country, material, 80, "WGI Score")
      y85 = rec_red(year, country, material, 85, "WGI Score")
      y90 = rec_red(year, country, material, 90, "WGI Score")
      y95 = rec_red(year, country, material, 95, "WGI Score")
      y100 = rec_red(year, country, material, 100, "WGI Score")

      x = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
      y = [y0, y5, y10, y15, y20, y25, y30, y35, y40, y45, y50, y55, y60, y65, y70, y75, y80, y85, y90, y95, y100]

      img = io.BytesIO()
      plt.plot(x, y)
      plt.savefig(img, format='png')
      img.seek(0)
      graph_url = base64.b64encode(img.getvalue()).decode()
      plt.close()
      return 'data:image/png;base64,{}'.format(graph_url)