import requests
import pandas as pd

def getData(lat, lon, sites, variables = ['temperature_2m','relative_humidity_2m','cloud_cover','wind_speed_10m','wind_direction_10m'], models = ['ecmwf_ifs025','ecmwf_aifs025','bom_access_global','gfs_global','ukmo_global_deterministic_10km'], pastDays = 0):
    """_summary_

    Args:
        lat (_type_): _description_
        lon (_type_): _description_
        sites (_type_): _description_
        variables (list, optional): _description_. Defaults to ['temperature_2m','wind_speed_10m'].

    Returns:
        _type_: _description_
    """
    if len(sites) > 1:
        lat = ','.join(lat)
        lon = ','.join(lon)
    else:
        lat = lat[0]
        lon = lon[0]
    variables = ','.join(variables)
    models = ','.join(models)

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly={variables}&models={models}&timezone=GMT&past_days={pastDays}"

    # Retrieve ECMWF temperatures
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

    else:
        print("Error retrieving ACCESS data from Open Meteo API.")

    def makeFrame(siteData):
        mdata = pd.DataFrame(siteData['hourly'])
        mdata.index = pd.to_datetime(mdata['time'])
        mdata = mdata.drop('time', axis =1)
        return mdata
    
    if len(sites) >1:
        dlist = []
        for d, site in zip(data, sites):
            df = makeFrame(d)
            df['site'] = site
            dlist.append(df)
        return pd.concat(dlist)

    return makeFrame(data)