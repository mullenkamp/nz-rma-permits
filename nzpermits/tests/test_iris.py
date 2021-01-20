# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 15:28:28 2018

@author: MichaelEK
"""
import numpy as np
import pandas as pd
import geopandas as gpd
from gistools import vector, util
from gistools import data_io

pd.options.display.max_columns = 10

####################################
### Parameters

base_url = 'https://maps.es.govt.nz/server/rest/services/Public/Consents/MapServer/'

layer_id = 22

#######################################
### Tests

data1 = data_io.query_esri_mapserver(base_url, layer_id)

d1 = data1['features'][1000]

geo1 = d1['geometry']
geo1['coordinates'] = np.round(geo1['coordinates'], 6).tolist()

condition = [{'condition_type': 'abstraction limit', 'limit': [{'value': d1['properties']['MaxAuthVolume_litres_sec'], 'period': 'S', 'units': 'l', 'limit_boundary': 'max'}]}]

station = [{'ref': d1['properties']['AbstractionSiteNo'], 'geometry': geo1}]

activity = [{'activity_type': 'consumptive take water', 'hydro_feature': 'groundwater', 'primary_purpose': d1['properties']['PrimaryIndustry'], 'station': station, 'condition': condition}]

permit = Permit(permit_id=d1['properties']['IRISID'], status=d1['properties']['CurrentStatus'], status_changed_date=pd.Timestamp(d1['properties']['CurrentStatusFromDate'], unit='ms'), commencement_date=pd.Timestamp(d1['properties']['CommencementDate'], unit='ms'), expiry_date=pd.Timestamp(d1['properties']['ExpiryDate'], unit='ms'), effective_end_date=pd.Timestamp(d1['properties']['AuthEffectiveEndDate'], unit='ms'), excercised=False, permitting_authority='Environment Southland', permit_type='water permit', activity=activity, modified_date=pd.Timestamp('2021-01-20'))




def test_sel_sites_poly():
    pts1 = vector.sel_sites_poly(sites_shp_path, rec_catch_shp_path, buffer_dis=10)

    assert (len(pts1) == 2) & isinstance(pts1, gpd.GeoDataFrame)












