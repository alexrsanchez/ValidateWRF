# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 21:35:41 2021

@author: aleja
"""

import cdsapi

c = cdsapi.Client()

c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis',
        'format': 'netcdf',
        'month': '02',
        'day': [
            '26', '27', '28',
        ],
        'year': '2019',
        'variable': [
            'total_cloud_cover', 'total_precipitation', '2m_temperature',
            '10m_u_component_of_wind', '10m_v_component_of_wind',
        ],
        'time': [
            '00:00', '01:00', '02:00',
            '03:00', '04:00', '05:00',
            '06:00', '07:00', '08:00',
            '09:00', '10:00', '11:00',
            '12:00', '13:00', '14:00',
            '15:00', '16:00', '17:00',
            '18:00', '19:00', '20:00',
            '21:00', '22:00', '23:00',
        ],
        'area': [
            46.1, -11.1, 35,
            4.9,
        ],
    },
    'ERA5_ESP09_20190226_20190228.nc')
