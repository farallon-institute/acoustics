#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def add_extra_columns_bio(fin):
    #add_space_time_columns
    #Add Date time in UTC to Data Frame
    #Add local time to Dataframe
    #local sunrise, sunset
    import shapely.geometry
    import pyproj
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import statistics as st
    import time as time
    from datetime import datetime
    from datetime import timedelta

    from astral import LocationInfo
    from astral.sun import sun
    
    import oceansdb

    import warnings
    warnings.filterwarnings(action='once')


    # Set up projections
    p_ll = pyproj.Proj(init='epsg:4326')#3310 #3488
    p_mt = pyproj.Proj(init='epsg:3857') # metric; same as EPSG:900913

    #fin='../../input_data/acoustic_reprocessing/20_line_testdata.csv'

    df1=pd.read_csv(fin)
    df1=df1.replace([-9999.0, 9999.0, -999.0, -9998, 999], np.nan)

    

    time_str=df1['Time_M']    
    dtime=list()
    sunrise=list()
    sunset=list()
#    suntime=list()
    totkrill=list()
    for i in range(len(df1['Time_M'])):
        if np.isnan(df1.loc[i]['Lat_M']):
            dtime.append(np.nan)
            totkrill.append(np.nan)
            sunrise.append(np.nan)
            sunset.append(np.nan)
            
        else:
            tmptime=df1.loc[i, 'Time_M']
            tmpdate=str(df1.loc[i, 'Date_M'])
            combo=tmpdate+tmptime
            dtime.append(datetime.strptime(combo, "%Y%m%d %H:%M:%S.%f"))
            
            tk=df1.loc[i, 'epac_biomass_fromABC'] + df1.loc[i, 'tspin_biomass_fromABC'] + df1.loc[i, 'ndiff_biomass_fromABC']
            totkrill.append(tk)
            
            lat=df1.loc[i]['Lat_M']
            lon=df1.loc[i]['Lon_M']
            l = LocationInfo('Pt Reyes', 'region', 'timezone/name', lat, lon)
            s=sun(l.observer, date=dtime[i]-timedelta(hours=7))
            sunrise.append(s['sunrise'] - timedelta(hours=7))
            sunset.append(s['sunset'] - timedelta(hours=7))
            
    df1['krill_biomass_fromABC']=totkrill
    df1['d_time_UTC']=dtime
    df1['d_time_local']=df1['d_time_UTC'] - timedelta(hours=7)
    df1['sunrise_local']=sunrise 
    df1['sunset_local']=sunset
    #Strips the seconds and milliseconds out of the datetime
    df1['sunrise_local']=df1['sunrise_local'].dt.floor('Min')
    df1['sunset_local']=df1['sunset_local'].dt.floor('Min')
    
    df1['d_time_local'] = df1['d_time_local'].dt.tz_localize(None)
    df1['sunrise_local'] = df1['sunrise_local'].dt.tz_localize(None)
    df1['sunset_local'] = df1['sunset_local'].dt.tz_localize(None)
        
    #Adds Suntime Variables after the other time variables have been added
    suntime=list()
    for i in range(len(df1['Time_M'])):
        if df1.loc[i]['d_time_local'].hour <= 12:
            suntime.append(df1.loc[i]['d_time_local']-df1.loc[i]['sunrise_local'])
        else:
            suntime.append(df1.loc[i]['sunset_local']-df1.loc[i]['d_time_local'])
    df1['suntime']=suntime
    suntime_hr=df1['suntime']/np.timedelta64(1, 'h')
    df1['suntime_hr']=suntime_hr
    
        #Adding Lat and Lon in Meters
    lons=df1['Lon_M']
    lats=df1['Lat_M']
    lon=lons.values.tolist()
    lat=lats.values.tolist()
    tdat=pyproj.transform(p_ll,p_mt,lon,lat)
    df1['lon_meters']=tdat[0]
    df1['lat_meters']=tdat[1]
    
    #Adding Bottom Depth
    odb = oceansdb.ETOPO()
    dep=list()
    for j in range(len(df1)):
        #Use these Lat Lons for "Statistics" Files
        lat=df1.iloc[j]['Lat_M']
        lon=df1.iloc[j]['Lon_M']
        if np.isnan(lat):
            dep.append(999)
        else:
            h = odb['topography'].extract(lat=lat, lon=lon)  #input needs to be lat=38, lon=-125
            depth=np.int(round(h['height'][0]))
            dep.append(depth)
    df1['Bottom_Depth']=dep
    
    #Creates New "Day_Only" Columns of Biomass, LogBiomass and NaN's nighttime data in those columns
    df1['krill_biomass_fromABC_dayonly']=df1['krill_biomass_fromABC']
    df1['epac_biomass_fromABC_dayonly']=df1['epac_biomass_fromABC']
    df1['tspin_biomass_fromABC_dayonly']=df1['tspin_biomass_fromABC']
    df1['ndiff_biomass_fromABC_dayonly']=df1['ndiff_biomass_fromABC']
    loar=df1['suntime_hr']<0.5
    df1.loc[loar,'krill_biomass_fromABC_dayonly']=np.nan
    df1.loc[loar,'epac_biomass_fromABC_dayonly']=np.nan
    df1.loc[loar,'tspin_biomass_fromABC_dayonly']=np.nan
    df1.loc[loar,'ndiff_biomass_fromABC_dayonly']=np.nan
    
    df1['log10_krill_biomass_fromABC']=np.log10(df1['krill_biomass_fromABC']+1)
    df1['log10_epac_biomass_fromABC']=np.log10(df1['epac_biomass_fromABC']+1)
    df1['log10_tspin_biomass_fromABC']=np.log10(df1['tspin_biomass_fromABC']+1)
    df1['log10_ndiff_biomass_fromABC']=np.log10(df1['ndiff_biomass_fromABC']+1)

    df1['log10_krill_biomass_fromABC_dayonly']=np.log10(df1['krill_biomass_fromABC_dayonly']+1)
    df1['log10_epac_biomass_fromABC_dayonly']=np.log10(df1['epac_biomass_fromABC_dayonly']+1)
    df1['log10_tspin_biomass_fromABC_dayonly']=np.log10(df1['tspin_biomass_fromABC_dayonly']+1)
    df1['log10_ndiff_biomass_fromABC_dayonly']=np.log10(df1['ndiff_biomass_fromABC_dayonly']+1)
    
    df1=df1.fillna(value=-9999.0)
    df1.to_csv (fin, index = False, header=True)

