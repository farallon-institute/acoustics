#!/usr/bin/env python
# coding: utf-8

# In[1]:


def final_depth_integrate_biomass_08252020(finname,foutname):

    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import statistics as st
    import time as time

    from IPython.core.interactiveshell import InteractiveShell
    InteractiveShell.ast_node_interactivity = "last"
    #other options include 'none', 'last', 'last_expr'

    df1=pd.read_csv(finname)  

    #df2=df1.copy(deep=True)
    #df2.drop(df2[df2[' Layer']!=2].index, inplace=True)
    #df2=df2.reset_index(drop=True)

    df1=df1.replace([-9999.0, 9999.0, -999.0], np.nan)
    df2=pd.DataFrame()
    interval=np.unique(df1['Interval'])
    for i in interval:
        minlayer=np.min(df1.loc[df1['Interval']==i,'Layer'])
        loar=((df1['Interval']==i) & (df1['Layer']==minlayer))
        df2=df2.append(df1[loar])

    df2=df2.reset_index(drop=True)

    #if 'Height_Mean' in df2.columns:
    #    del df2['Height_Mean']

    if 'Depth_Mean' in df2.columns:
        del df2['Depth_Mean']

    df2.rename({'Height_Mean': 'Total_Depth_Sampled'}, axis=1, inplace=True)

    bad_value=-9998
    tic=time.time()
    cnt=0  #Counter is needed in case interval is not sequential in the original csv file
    for i in interval:
        if any(df1['Interval']==i):
            #print(i)
            loar=df1['Interval']==i
            #idx=loar[loar==True].index[-1]  #Maybe Not Needed
            #df2[' NASC'][i]=sum((df1[' NASC'])[loar])  #THis Created Warnings!  Better to use iloc like below
            if pd.isnull(df1[loar]['NASC']).all():  #If all values are NAN's
                df2.iloc[cnt,df2.columns.get_loc('Sv_Mean')]=bad_value
                df2.iloc[cnt,df2.columns.get_loc('NASC')]=np.nan
                df2.iloc[cnt,df2.columns.get_loc('ABC')]=np.nan
                df2.iloc[cnt,df2.columns.get_loc('Layer_Depth_Max')]=np.nan
                df2.iloc[cnt,df2.columns.get_loc('Layer_Depth_Min')]=np.nan

                df2.iloc[cnt,df2.columns.get_loc('Total_Depth_Sampled')]=np.nan

                df2.iloc[cnt,df2.columns.get_loc('Beam_Volume')]=np.nan

                df2.iloc[cnt,df2.columns.get_loc('epac_#krill_fromNASC')]=np.nan
                df2.iloc[cnt,df2.columns.get_loc('epac_#krill_fromABC')]=np.nan
                df2.iloc[cnt,df2.columns.get_loc('epac_#krill_fromSv')]=np.nan
                df2.iloc[cnt,df2.columns.get_loc('epac_biomass_fromNASC')]=np.nan
                df2.iloc[cnt,df2.columns.get_loc('epac_biomass_fromABC')]=np.nan
                df2.iloc[cnt,df2.columns.get_loc('epac_biomass_fromSv')]=np.nan

                df2.iloc[cnt,df2.columns.get_loc('tspin_#krill_fromNASC')]=np.nan
                df2.iloc[cnt,df2.columns.get_loc('tspin_#krill_fromABC')]=np.nan
                df2.iloc[cnt,df2.columns.get_loc('tspin_#krill_fromSv')]=np.nan
                df2.iloc[cnt,df2.columns.get_loc('tspin_biomass_fromNASC')]=np.nan
                df2.iloc[cnt,df2.columns.get_loc('tspin_biomass_fromABC')]=np.nan
                df2.iloc[cnt,df2.columns.get_loc('tspin_biomass_fromSv')]=np.nan

                df2.iloc[cnt,df2.columns.get_loc('ndiff_#krill_fromNASC')]=np.nan
                df2.iloc[cnt,df2.columns.get_loc('ndiff_#krill_fromABC')]=np.nan
                df2.iloc[cnt,df2.columns.get_loc('ndiff_#krill_fromSv')]=np.nan
                df2.iloc[cnt,df2.columns.get_loc('ndiff_biomass_fromNASC')]=np.nan
                df2.iloc[cnt,df2.columns.get_loc('ndiff_biomass_fromABC')]=np.nan
                df2.iloc[cnt,df2.columns.get_loc('ndiff_biomass_fromSv')]=np.nan
                cnt=cnt+1
            else:
                df2.iloc[cnt,df2.columns.get_loc('Sv_Mean')]=bad_value
                df2.iloc[cnt,df2.columns.get_loc('NASC')]=np.sum((df1['NASC'])[loar])
                df2.iloc[cnt,df2.columns.get_loc('ABC')]=np.sum((df1['ABC'])[loar])
                df2.iloc[cnt,df2.columns.get_loc('Layer_Depth_Max')]=np.nanmax((df1['Layer_Depth_Max'])[loar])
                df2.iloc[cnt,df2.columns.get_loc('Layer_Depth_Min')]=np.nanmin((df1['Layer_Depth_Min'])[loar])

                loar2=((df1['Interval']==i) & (~np.isnan(df1['NASC'])))
                np.sum(loar2)
                df2.iloc[cnt,df2.columns.get_loc('Total_Depth_Sampled')]=np.sum(loar2)*10

                df2.iloc[cnt,df2.columns.get_loc('Beam_Volume')]=np.sum((df1['Beam_Volume'])[loar])

                df2.iloc[cnt,df2.columns.get_loc('epac_#krill_fromNASC')]=np.sum((df1['epac_#krill_fromNASC'])[loar])
                df2.iloc[cnt,df2.columns.get_loc('epac_#krill_fromABC')]=np.sum((df1['epac_#krill_fromABC'])[loar])
                df2.iloc[cnt,df2.columns.get_loc('epac_#krill_fromSv')]=np.sum((df1['epac_#krill_fromSv'])[loar])
                df2.iloc[cnt,df2.columns.get_loc('epac_biomass_fromNASC')]=np.sum((df1['epac_biomass_fromNASC'])[loar])
                df2.iloc[cnt,df2.columns.get_loc('epac_biomass_fromABC')]=np.sum((df1['epac_biomass_fromABC'])[loar])
                df2.iloc[cnt,df2.columns.get_loc('epac_biomass_fromSv')]=np.sum((df1['epac_biomass_fromSv'])[loar])

                df2.iloc[cnt,df2.columns.get_loc('tspin_#krill_fromNASC')]=np.sum((df1['tspin_#krill_fromNASC'])[loar])
                df2.iloc[cnt,df2.columns.get_loc('tspin_#krill_fromABC')]=np.sum((df1['tspin_#krill_fromABC'])[loar])
                df2.iloc[cnt,df2.columns.get_loc('tspin_#krill_fromSv')]=np.sum((df1['tspin_#krill_fromSv'])[loar])
                df2.iloc[cnt,df2.columns.get_loc('tspin_biomass_fromNASC')]=np.sum((df1['tspin_biomass_fromNASC'])[loar])
                df2.iloc[cnt,df2.columns.get_loc('tspin_biomass_fromABC')]=np.sum((df1['tspin_biomass_fromABC'])[loar])
                df2.iloc[cnt,df2.columns.get_loc('tspin_biomass_fromSv')]=np.sum((df1['tspin_biomass_fromSv'])[loar])

                df2.iloc[cnt,df2.columns.get_loc('ndiff_#krill_fromNASC')]=np.sum((df1['ndiff_#krill_fromNASC'])[loar])
                df2.iloc[cnt,df2.columns.get_loc('ndiff_#krill_fromABC')]=np.sum((df1['ndiff_#krill_fromABC'])[loar])
                df2.iloc[cnt,df2.columns.get_loc('ndiff_#krill_fromSv')]=np.sum((df1['ndiff_#krill_fromSv'])[loar])
                df2.iloc[cnt,df2.columns.get_loc('ndiff_biomass_fromNASC')]=np.sum((df1['ndiff_biomass_fromNASC'])[loar])
                df2.iloc[cnt,df2.columns.get_loc('ndiff_biomass_fromABC')]=np.sum((df1['ndiff_biomass_fromABC'])[loar])
                df2.iloc[cnt,df2.columns.get_loc('ndiff_biomass_fromSv')]=np.sum((df1['ndiff_biomass_fromSv'])[loar])
                cnt=cnt+1
                #tmp_date=df[' Date_M'][loar]
                #f_time.append((df[' Time_M'])[loar])

    toc=time.time()
    elapsed=toc-tic
    #print(elapsed)


    df2=df2.fillna(value=-9999.0)
    df2.to_csv (foutname, index = False, header=True)
    print('Writing ' + foutname + ' with     ' + str(len(df2.index)) + ' rows.') 
    print('Processing took ' + str(elapsed) + ' seconds.')
    print('')

