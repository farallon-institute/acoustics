#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def krill_biomass_07212020(finname,foutname):
    
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import statistics as st
    import time as time
    import pyreadr
    import oceansdb
    from shapely.geometry import Point
    from shapely.geometry.polygon import Polygon
    import geopandas as gpd
    import sys


    from IPython.core.interactiveshell import InteractiveShell
    InteractiveShell.ast_node_interactivity = "last"
    
    base='/Users/jeffdorman/Documents/python/krill_biomass/'
    #Load NASC Data
    #fname = '../../input_data/acoustic_reprocessing/JRS_2014_reprocessed/20140530_reprocessed.csv'
    #fname='../../input_data/acoustic_reprocessing/20_line_testdata.csv'
    tic=time.time()
    df1=pd.read_csv(finname)
    df1=df1.replace([-9999.0, 9999.0], np.nan)


    #Load Length Frequency Data
    #Euphausia pacifica
    fname = base + 'input_data/LF_data/epClimatology_S2raw_2011-18_07202020.csv'
    epLF=pd.read_csv(fname)
    epLF=epLF.replace(np.nan, 0)
    #Thysanoessa spinifera
    fname = base + 'input_data/LF_data/tsClimatology_S2raw_2011-18_07202020.csv'
    tsLF=pd.read_csv(fname)
    tsLF=tsLF.replace(np.nan, 0)
    #Nematoscelis Difficilis
    fname = base + 'input_data/LF_data/ndClimatology_S2raw_2011-18_07202020.csv'
    ndLF=pd.read_csv(fname)
    ndLF=ndLF.replace(np.nan, 0)

    #Load TS/BS Data
    #Euphausia pacifica
    fname= base + 'input_data/TS_data/mean_ep_BS_data_20200528.csv'
    epTSBS=pd.read_csv(fname, header=None)
    epTSBS.rename(columns={"0":"length","1":"meanBS","2":"std_dev", "3":"std_err"})
    #Thysanoessa spinifera
    fname= base + 'input_data/TS_data/mean_ts_BS_data_20200528.csv'
    tsTSBS=pd.read_csv(fname, header=None)
    tsTSBS.rename(columns={"0":"length","1":"meanBS","2":"std_dev", "3":"std_err"})
    #Nematoscelis difficilis
    fname= base + 'input_data/TS_data/mean_nd_BS_data_20200528.csv'
    ndTSBS=pd.read_csv(fname, header=None)
    ndTSBS.rename(columns={"0":"length","1":"meanBS","2":"std_dev", "3":"std_err"})

    #Load COMMUNITY COMPOSITION Data
    fname= base + 'input_data/community_composition/CC_Depth_GAM_North_2002to2018_20200610.csv'
    ccNorth=pd.read_csv(fname)
    fname= base + 'input_data/community_composition/CC_Depth_GAM_NorthCentral_2002to2018_20200610.csv'
    ccNorthCentral=pd.read_csv(fname)
    fname= base + 'input_data/community_composition/CC_Depth_GAM_Central_2002to2018_20200610.csv'
    ccCentral=pd.read_csv(fname)
    #fname='../../input_data/community_composition/CC_Depth_GAM_South_2002to2018_20200610.csv'
    fname= base + 'input_data/community_composition/CC_Depth_GAM_South_2015to2018_20200626.csv'
    ccSouth=pd.read_csv(fname)

    #Calculates DW for the size classes of each species (10 to 34 mm)
    #epDW=(epTSBS.loc[0:24,0]**3.239)*.000795
    #tsDW=(tsTSBS.loc[0:24,0]**3.0212)*.0012
    #ndDW=

    #Wet Weight Calculations, using equations from Joe and Brandyn.  ND calculation comes from a relationship
    #developed for all krill as they didn't collect enought N.Difficilis to develop a robust relationship.
    epWW=(10**-1.5)*(epTSBS.loc[0:24,0]**2.56)
    tsWW=(10**-2.7)*(tsTSBS.loc[0:24,0]**3.67)
    ndWW=(10**-2)*(ndTSBS.loc[0:24,0]**3.04)


    odb = oceansdb.ETOPO()

    #Create a Region Column for the Acoustic Data.
    #North = 0  [>=38 Latitude]
    #NorthCentral = 1  [>=36.3 & , <38 Latitude]
    #Central = 2  [>=34.45 & , <36.3 Latitude]
    #South = 3  [<34.45 Latitude]
    rw=len(df1)
    reg_list=[999]*rw
    df1['region']=reg_list

    loar=df1[' Lat_M']>38
    df1.at[loar.values, 'region']=0
    loar=((df1[' Lat_M']>=36.3) & (df1[' Lat_M']<38))
    df1.at[loar.values, 'region']=1
    loar=((df1[' Lat_M']>=34.45) & (df1[' Lat_M']<36.3))
    df1.at[loar.values, 'region']=2
    loar=df1[' Lat_M']<34.45
    df1.at[loar.values, 'region']=3

    loar=df1['region']==999
    if sum(loar)>0:
        print ('Houston we have a problem')
        sys.exit("Cell 1, Line 90")


    # In[2]:


    #This Code sums up offshore and onshore data from the North, NorthCentral, Central, and South.
    #Then changes the values to percentages

    #Epac North LENGTH FREQUENCIES
    epN=epLF.iloc[0][3:].values+epLF.iloc[1][3:].values
    epN_pct=epN/sum(epN)
    #Epac NorthCentral
    epNC=epLF.iloc[2][3:].values+epLF.iloc[3][3:].values
    epNC_pct=epNC/sum(epNC)
    #Epac Central
    epC=epLF.iloc[4][3:].values+epLF.iloc[5][3:].values
    epC_pct=epC/sum(epC)
    #Epac South
    epS=epLF.iloc[6][3:].values+epLF.iloc[7][3:].values
    epS_pct=epS/sum(epS)

    #Tspin North LENGTH FREQUENCIES
    tsN=tsLF.iloc[0][3:].values+tsLF.iloc[1][3:].values
    tsN_pct=tsN/sum(tsN)
    #Tspin NorthCentral
    tsNC=tsLF.iloc[2][3:].values+tsLF.iloc[3][3:].values
    tsNC_pct=tsNC/sum(tsNC)
    #Tspin Central
    tsC=tsLF.iloc[4][3:].values+tsLF.iloc[5][3:].values
    tsC_pct=tsC/sum(tsC)
    #Tspin South
    tsS=tsLF.iloc[6][3:].values+tsLF.iloc[7][3:].values
    tsS_pct=tsS/sum(tsS)

    #Ndiff North LENGTH FREQUENCIES
    ndN=ndLF.iloc[0][3:].values+ndLF.iloc[1][3:].values
    ndN_pct=ndN/sum(ndN)
    #Ndiff NorthCentral
    ndNC=ndLF.iloc[2][3:].values+ndLF.iloc[3][3:].values
    ndNC_pct=ndNC/sum(ndNC)
    #Ndiff Central
    ndC=ndLF.iloc[4][3:].values+ndLF.iloc[5][3:].values
    ndC_pct=ndC/sum(ndC)
    #Ndiff South
    ndS=ndLF.iloc[6][3:].values+ndLF.iloc[7][3:].values
    ndS_pct=ndS/sum(ndS)

    #Creates Regional Mean BACKSCATTERING STRENGTH based on the L/F Data Available.
    epBS=epTSBS.iloc[0:-1][1].values
    epBSN=sum(epBS*epN_pct)
    epBSNC=sum(epBS*epNC_pct)
    epBSC=sum(epBS*epC_pct)
    epBSS=sum(epBS*epS_pct)

    tsBS=tsTSBS.iloc[0:-1][1].values
    tsBSN=sum(tsBS*tsN_pct)
    tsBSNC=sum(tsBS*tsNC_pct)
    tsBSC=sum(tsBS*tsC_pct)
    tsBSS=sum(tsBS*tsS_pct)

    ndBS=ndTSBS.iloc[0:-1][1].values
    ndBSN=sum(ndBS*ndN_pct)
    ndBSNC=sum(ndBS*ndNC_pct)
    ndBSC=sum(ndBS*ndC_pct)

    ndBSS=sum(ndBS*ndS_pct)


    # In[10]:


    
    old_reg=999  # This will get updated based on the lat lon data below

    epnkN=list()
    epnkA=list()
    epnkSv=list()
    #epnkSveqABC=list()
    #epnkSveqNASC=list()
    epbiomassN=list()
    epbiomassA=list()
    epbiomassSv=list()
    tsnkN=list()
    tsnkA=list()
    tsnkSv=list()
    #tsnkSveqABC=list()
    #tsnkSveqNASC=list()
    tsbiomassN=list()
    tsbiomassA=list()
    tsbiomassSv=list()
    ndnkN=list()
    ndnkA=list()
    ndnkSv=list()
    #ndnkSveqABC=list()
    #ndnkSveqNASC=list()
    ndbiomassN=list()
    ndbiomassA=list()
    ndbiomassSv=list()

    for i in df1.index:
        #Get NASC
        nasc=df1[' NASC'][i]
        abc=df1[' ABC'][i]
        sv=df1[' Sv_mean'][i]
        svlin=10**(sv/10)
        #This has been added in because there are a few random 999.0's in Lat and Lon
        lon=df1[' Lon_M'][i]
        lat=df1[' Lat_M'][i]

        if ((np.isnan(nasc)) | (lat>100) | (lon>200)):  #If no data, move on
            #update Counters and put nan's in the output file
            epnkN.append(np.nan)
            epnkA.append(np.nan)
            epnkSv.append(np.nan)
            #epnkSveqABC.append(np.nan)
            #epnkSveqNASC.append(np.nan)
            epbiomassN.append(np.nan)
            epbiomassA.append(np.nan)
            epbiomassSv.append(np.nan)
            tsnkN.append(np.nan)
            tsnkA.append(np.nan)
            tsnkSv.append(np.nan)
            #tsnkSveqABC.append(np.nan)
            #tsnkSveqNASC.append(np.nan)
            tsbiomassN.append(np.nan)
            tsbiomassA.append(np.nan)
            tsbiomassSv.append(np.nan)
            ndnkN.append(np.nan)
            ndnkA.append(np.nan)
            ndnkSv.append(np.nan)
            #ndnkSveqABC.append(np.nan)
            #ndnkSveqNASC.append(np.nan)
            ndbiomassN.append(np.nan)
            ndbiomassA.append(np.nan)
            ndbiomassSv.append(np.nan)
            continue
        elif nasc==0:
                    #update Counters and put nan's in the output file
            epnkN.append(0)
            epnkA.append(0)
            epnkSv.append(0)
            #epnkSveqABC.append(0)
            #epnkSveqNASC.append(0)
            epbiomassN.append(0)
            epbiomassA.append(0)
            epbiomassSv.append(0)
            tsnkN.append(0)
            tsnkA.append(0)
            tsnkSv.append(0)
            #tsnkSveqABC.append(0)
            #tsnkSveqNASC.append(0)
            tsbiomassN.append(0)
            tsbiomassA.append(0)
            tsbiomassSv.append(0)
            ndnkN.append(0)
            ndnkA.append(0)
            ndnkSv.append(0)
            #ndnkSveqABC.append(0)
            #ndnkSveqNASC.append(0)
            ndbiomassN.append(0)
            ndbiomassA.append(0)
            ndbiomassSv.append(0)

        else:
            #Get Longitude, Latitude, Region
            lon=df1[' Lon_M'][i]
            lat=df1[' Lat_M'][i]
            reg=df1['region'][i]
            thick=df1[' Thickness_mean'][i]
            if old_reg==reg:
                #No Updating Needed
                pass
            else:
                if reg==0:
                    cc=ccNorth
                    epBS=epBSN
                    tsBS=tsBSN
                    ndBS=ndBSN
                    ep_pct=epN_pct
                    ts_pct=tsN_pct
                    nd_pct=ndN_pct
                elif reg==1:
                    cc=ccNorthCentral
                    epBS=epBSNC
                    tsBS=tsBSNC
                    ndBS=ndBSNC
                    ep_pct=epNC_pct
                    ts_pct=tsNC_pct
                    nd_pct=ndNC_pct
                elif reg==2:
                    cc=ccCentral
                    epBS=epBSC
                    tsBS=tsBSC
                    ndBS=ndBSC
                    ep_pct=epC_pct
                    ts_pct=tsC_pct
                    nd_pct=ndC_pct
                elif reg==3:
                    cc=ccSouth
                    epBS=epBSS
                    tsBS=tsBSS
                    ndBS=ndBSS
                    ep_pct=epS_pct
                    ts_pct=tsS_pct
                    nd_pct=ndS_pct
                else:
                    print('No Region Detected.  Should Never Get Here')
                    sys.exit("Cell 3, Line 58")

            #Determine the Depth
            #print('i= ' + str(i) + '. Lat Lon = ' + str(lat) + ' ' + str(lon))
            h = odb['topography'].extract(lat=lat, lon=lon)  #input needs to be lat=38, lon=-125
            #depth=np.int(round(h['height'][0])*-1)
            depth=np.int(abs(round(h['height'][0])))
            
            #Determine the Euphausia pacifica vs Thysanoessa spinifera split
            if reg==3:
                if depth>1000:
                    ts_ratio=cc['Tspin_Ratio'][1000]
                    ep_ratio=cc['Epac_Ratio'][1000]
                    nd_ratio=cc['Ndiff_Ratio'][1000]
                else:
                    ts_ratio=cc['Tspin_Ratio'][depth]
                    ep_ratio=cc['Epac_Ratio'][depth]
                    nd_ratio=cc['Ndiff_Ratio'][depth]

            else:
                if depth>1000:
                    ts_ratio=cc['Tspin_to_Epac_Ratio'][1000]
                    ep_ratio=1-ts_ratio
                    nd_ratio=0
                else:
                    ts_ratio=cc['Tspin_to_Epac_Ratio'][depth]
                    ep_ratio=1-ts_ratio
                    nd_ratio=0

            #Determine the amount of NASC for each Group
            ep_nasc=nasc*(ep_ratio)
            ts_nasc=nasc*(ts_ratio)
            nd_nasc=nasc*(nd_ratio)
            ep_abc=abc*(ep_ratio)
            ts_abc=abc*(ts_ratio)
            nd_abc=abc*(nd_ratio)
            ep_svlin=svlin*(ep_ratio)
            ts_svlin=svlin*(ts_ratio)
            nd_svlin=svlin*(nd_ratio)



            epnkN.append(ep_nasc/(epBS*4*np.pi))
            epnkA.append(ep_abc/epBS)
            epnkSv.append(ep_svlin/epBS)
            #epnkSveqABC.append((ep_svlin/epBS)*thick)
            #epnkSveqNASC.append(((ep_svlin/epBS)*thick)*(1852**2))
            epnkLFN=(ep_nasc/epBS)*ep_pct
            epnkLFA=(ep_abc/epBS)*ep_pct
            epnkLFSv=(ep_svlin/epBS)*ep_pct
            epbiomassN.append(sum(epnkLFN*epWW))
            epbiomassA.append(sum(epnkLFA*epWW))
            epbiomassSv.append(sum(epnkLFSv*epWW))

            tsnkN.append(ts_nasc/(tsBS*4*np.pi))
            tsnkA.append(ts_abc/tsBS)
            tsnkSv.append(ts_svlin/tsBS)
            #tsnkSveqABC.append((ts_svlin/tsBS)*thick)
            #tsnkSveqNASC.append(((ts_svlin/tsBS)*thick)*(1852**2))
            tsnkLFN=(ts_nasc/tsBS)*ts_pct
            tsnkLFA=(ts_abc/tsBS)*ts_pct
            tsnkLFSv=(ts_svlin/tsBS)*ts_pct
            tsbiomassN.append(sum(tsnkLFN*tsWW))
            tsbiomassA.append(sum(tsnkLFA*tsWW))
            tsbiomassSv.append(sum(tsnkLFSv*tsWW))

            ndnkN.append(nd_nasc/(ndBS*4*np.pi))
            ndnkA.append(nd_abc/ndBS)
            ndnkSv.append(nd_svlin/ndBS)
            #ndnkSveqABC.append((nd_svlin/ndBS)*thick)
            #ndnkSveqNASC.append(((nd_svlin/ndBS)*thick)*(1852**2))
            ndnkLFN=(nd_nasc/ndBS)*nd_pct
            ndnkLFA=(nd_abc/ndBS)*nd_pct
            ndnkLFSv=(nd_svlin/ndBS)*nd_pct
            ndbiomassN.append(sum(ndnkLFN*ndWW))
            ndbiomassA.append(sum(ndnkLFA*ndWW))
            ndbiomassSv.append(sum(ndnkLFSv*ndWW))





            #tsnk.append(ts_nasc/tsBS)
            #tsnkLF=(ts_nasc/tsBS)*ts_pct
            #tsbiomass.append(sum(tsnkLF*tsDW))


            old_reg=reg




    # In[11]:


    finaldf = pd.DataFrame(
        {'Interval': df1[' Interval'],
         'Layer': df1[' Layer'],
         'Sv_Mean': df1[' Sv_mean'],
         'NASC': df1[' NASC'],
         'ABC': df1[' ABC'],
         'Height_Mean': df1[' Height_mean'],
         'Depth_Mean': df1[' Depth_mean'],
         'Layer_Depth_Min': df1[' Layer_depth_min'],
         'Layer_Depth_Max': df1[' Layer_depth_max'],
         'Date_M': df1[' Date_M'],
         'Time_M': df1[' Time_M'],
         'Lon_M': df1[' Lon_M'],
         'Lat_M': df1[' Lat_M'],
         'Beam_Volume': df1[' Beam_volume_sum'],     
         'epac_#krill_fromNASC': epnkN,
         'epac_#krill_fromABC': epnkA,
         'epac_#krill_fromSv': epnkSv,
         'epac_biomass_fromNASC': epbiomassN,
         'epac_biomass_fromABC': epbiomassA,
         'epac_biomass_fromSv': epbiomassSv,
         'tspin_#krill_fromNASC': tsnkN,
         'tspin_#krill_fromABC': tsnkA,
         'tspin_#krill_fromSv': tsnkSv,
         'tspin_biomass_fromNASC': tsbiomassN,
         'tspin_biomass_fromABC': tsbiomassA,
         'tspin_biomass_fromSv': tsbiomassSv,
         'ndiff_#krill_fromNASC': ndnkN,
         'ndiff_#krill_fromABC': ndnkA,
         'ndiff_#krill_fromSv': ndnkSv,
         'ndiff_biomass_fromNASC': ndbiomassN,
         'ndiff_biomass_fromABC': ndbiomassA,
         'ndiff_biomass_fromSv': ndbiomassSv
        })

    finaldf=finaldf.replace(np.nan, -9999)

    #foutname='../../output_data/acoustic_biomass/2014/20140530_biomass.csv'
    finaldf.to_csv (foutname, index = False, header=True)
    toc=time.time()
    print('Writing ' + foutname) 
    print('Processing took ' +str(toc-tic)+ ' seconds.')
    print('')
    
    

