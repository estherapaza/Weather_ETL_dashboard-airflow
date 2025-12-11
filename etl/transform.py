# import libraries
import pandas as pd

# transforms weather data
def transform_data(dfs):
    # data extraction - temperature
    df_temp = dfs['temperature']
    df_temp['date'] = df_temp['datetime'].dt.strftime('%d/%m/%Y')

    # daily min - max temperatures
    daily_temps = (
        df_temp.groupby('date')['temperature_2m']
        .agg(['min', 'max'])
        .rename(columns={'min': 'Temperatura Minima', 'max': 'Temperatura Massima'})
        .reset_index()
        .rename(columns={'date': 'Data'})
    )
    daily_temps['Data'] = pd.to_datetime(daily_temps['Data'], format='%d/%m/%Y')
    daily_temps['Data'] = daily_temps['Data'].dt.strftime('%d/%m/%Y')

    # merge hourly data for transformation
    df_merged = df_temp.copy()
    for key in ['humidity', 'precipitation', 'wind']:
        df_merged = pd.merge(df_merged, dfs[key], on='datetime', how='outer')

    df_merged = df_merged.sort_values('datetime').ffill().bfill()

    # formatting date, time, and time slots
    df_merged['Data'] = df_merged['datetime'].dt.strftime('%d/%m/%Y')
    df_merged['Ora'] = df_merged['datetime'].dt.strftime('%H:%M')

    def get_period(ora):
        h = int(ora.split(':')[0])
        if 6 <= h < 12: return 'Mattina' # morning
        elif 12 <= h < 18: return 'Pomeriggio' # afternoon
        elif 18 <= h < 24: return 'Sera' # evening
        return 'Notte' # night

    df_merged['Fascia Oraria'] = df_merged['Ora'].apply(get_period)

    # renaming columns
    df_merged.rename(columns={
        'temperature_2m': 'Temperatura (°C)',
        'apparent_temperature': 'Temperatura Percepita (°C)',
        'relative_humidity_2m': 'Umidità (%)',
        'precipitation': 'Precipitazioni (mm)',
        'precipitation_probability': 'Probabilità di Precipitazione',
        'windspeed_10m': 'Velocità Vento (km/h)',
        'windgusts_10m': 'Raffiche di Vento (km/h)'
    }, inplace=True)

    # weather alert classifications
    def classify_weather(row):
        if row['Precipitazioni (mm)'] > 10:
            return "Pioggia intensa" # heavy rain
        elif row['Velocità Vento (km/h)'] > 50:
            return "Vento forte" # strong wind
        elif row['Temperatura (°C)'] > 35:
            return "Caldo estremo" # extreme heat
        elif row['Temperatura (°C)'] < 0:
            return "Freddo estremo" # extreme cold
        return "Normale" # normal

    df_merged['Allerta Meteo'] = df_merged.apply(classify_weather, axis=1)

    # separate tables
    base_cols = ['datetime', 'Data', 'Ora']
    temperature_hourly = df_merged[base_cols + ['Temperatura (°C)', 'Temperatura Percepita (°C)']]
    precipitation_hourly = df_merged[base_cols + ['Precipitazioni (mm)', 'Probabilità di Precipitazione']]
    humidity_hourly = df_merged[base_cols + ['Umidità (%)']]
    wind_hourly = df_merged[base_cols + ['Velocità Vento (km/h)', 'Raffiche di Vento (km/h)']]

    # weather alert
    alerts_df = (
        df_merged[df_merged['Allerta Meteo'] != 'Normale']
        [['Data', 'Fascia Oraria', 'Allerta Meteo']]
        .drop_duplicates()
        .sort_values('Data')
        .reset_index(drop=True)
    )

    alerts_df.to_csv('/opt/airflow/data/weather_alerts.csv', index=False)

    # returns tables ready for loading
    return (
        df_merged,
        daily_temps,
        temperature_hourly,
        precipitation_hourly,
        humidity_hourly,
        wind_hourly,
        alerts_df
    )