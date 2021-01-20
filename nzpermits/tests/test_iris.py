# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 15:28:28 2018

@author: MichaelEK
"""
import pandas as pd
import geopandas as gpd
from gistools import vector, util
from gistools.datasets import get_path

pd.options.display.max_columns = 10

####################################
### Parameters

sites_shp = 'flow_recorders_pareora'
rec_streams_shp = 'rec_streams_pareora'
rec_catch_shp = 'rec_catch_pareora'
catch_shp = 'catchment_pareora'

sites_shp_path = get_path(sites_shp)
rec_streams_shp_path = get_path(rec_streams_shp)
rec_catch_shp_path = get_path(rec_catch_shp)
catch_shp_path = get_path(catch_shp)

sites_col_name = 'SITENUMBER'
poly_col_name = 'Catchmen_1'
line_site_col = 'NZREACH'

#######################################
### Tests

pts = util.load_geo_data(sites_shp_path)
pts['geometry'] = pts.geometry.simplify(1)
rec_streams1 = util.load_geo_data(rec_streams_shp_path)
rec_pts1 = rec_streams1.copy()
rec_pts1['geometry'] = rec_streams1.centroid


def test_sel_sites_poly():
    pts1 = vector.sel_sites_poly(sites_shp_path, rec_catch_shp_path, buffer_dis=10)

    assert (len(pts1) == 2) & isinstance(pts1, gpd.GeoDataFrame)

def test_pts_poly_join():
    pts2, poly2 = vector.pts_poly_join(sites_shp_path, catch_shp_path, poly_col_name)

    assert (len(pts2) == 2) & (len(poly2) == 1) & isinstance(pts2, gpd.GeoDataFrame)

def test_xy_to_gpd():
    pts_df = pts[[sites_col_name, 'geometry']].copy()
    pts_df['x'] = pts_df.geometry.x
    pts_df['y'] = pts_df.geometry.y
    pts_df.drop('geometry', axis=1, inplace=True)

    pts3 = vector.xy_to_gpd(sites_col_name, 'x', 'y', pts_df)

    assert (len(pts3) == 2) & isinstance(pts3, gpd.GeoDataFrame)

def test_closest_line_to_pts():
    line1 = vector.closest_line_to_pts(sites_shp_path, rec_streams_shp_path, line_site_col)

    assert (len(line1) == 2) & isinstance(line1, gpd.GeoDataFrame) & line1[line_site_col].notnull().all()


def test_kd_nearest():
    line2 = vector.kd_nearest(pts, rec_pts1, line_site_col)

    assert (len(line2) == 2) & isinstance(line2, gpd.GeoDataFrame) & line2[line_site_col].notnull().all()










