# import libraries
import altair as alt
import pandas as pd

# temperature - hourly chart
def temperature_hourly_chart(df):
    # converts the dataframe to "long" format to draw two lines (actual and felt temperature)
    df_orarie_long = df.melt(
        id_vars=["datetime", "Data", "Ora"],
        value_vars=["Temperatura (°C)", "Temperatura Percepita (°C)"],
        var_name="Tipo",
        value_name="Valore",
    )

    # line chart with interactive points
    chart = (
        alt.Chart(df_orarie_long)
        .mark_line(point=True)
        .encode(
            x=alt.X("datetime:T", title="Ora", axis=alt.Axis(format="%H:%M")),
            y=alt.Y("Valore:Q", title="Temperatura (°C)"),
            color=alt.Color(
                "Tipo:N",
                scale=alt.Scale(
                    domain=["Temperatura (°C)", "Temperatura Percepita (°C)"],
                    range=["crimson", "darkorange"],
                ),
            ),
            tooltip=["Ora", "Tipo", "Valore"],
        )
        .properties(title=f"real and felt temperature - {df['Data'].iloc[0]}")
        .interactive()
    )
    return chart

# temperature - weekly hourly chart
def temperature_weekly_chart(df):
    chart = (
        alt.Chart(df)
        .mark_line(color="firebrick")
        .encode(
            x=alt.X("datetime:T", title="Data/Ora"),
            y=alt.Y("Temperatura (°C):Q"),
            tooltip=["Data", "Ora", "Temperatura (°C)"],
        )
        .properties(title="hourly temperature - week")
        .interactive()
    )
    return chart

# temperature - daily minimum and maximum
def temperature_daily_min_max_chart(df):
    # fold to transform from wide to long: two lines (minimum and maximum)
    chart = (
        alt.Chart(df.dropna())
        .transform_fold(
            ["Temperatura Minima", "Temperatura Massima"], as_=["Tipo", "Valore"]
        )
        .mark_line(point=True, size=3)
        .encode(
            x=alt.X("Data:T", title="Data", axis=alt.Axis(format="%d/%m")),
            y=alt.Y("Valore:Q", title="Temperatura (°C)"),
            color=alt.Color(
                "Tipo:N",
                scale=alt.Scale(
                    domain=["Temperatura Minima", "Temperatura Massima"],
                    range=["#0033cc", "#cc3300"],
                ),
                title=None,
            ),
            tooltip=["Data:T", "Tipo:N", "Valore:Q"],
        )
        .properties(title="minimum and maximum temperature - week")
        .interactive()
    )
    return chart

# precipitation - daily
def precipitation_daily_chart(df_oggi):
    # bar chart: rain quantity
    chart_mm = (
        alt.Chart(df_oggi)
        .mark_bar(color="steelblue")
        .encode(
            x=alt.X("datetime:T", title="Ora", axis=alt.Axis(format="%H:%M")),
            y=alt.Y("Precipitazioni (mm):Q"),
            tooltip=["Ora", "Precipitazioni (mm)"],
        )
        .properties(title=f"precipitation and probability - {df_oggi['Data'].iloc[0]}")
        .interactive()
    )

    # line: rain probability
    chart_prob_line = (
        alt.Chart(df_oggi)
        .mark_line(color="orange")
        .encode(
            x=alt.X("datetime:T", title="Ora", axis=alt.Axis(format="%H:%M")),
            y=alt.Y("Probabilità di Precipitazione:Q"),
            tooltip=["Ora", "Probabilità di Precipitazione"],
        )
        .interactive()
    )

    # points on the line
    chart_prob_points = (
        alt.Chart(df_oggi)
        .mark_point(color="orange", filled=True, size=60)
        .encode(
            x=alt.X("datetime:T"),
            y=alt.Y("Probabilità di Precipitazione:Q"),
            tooltip=["Ora", "Probabilità di Precipitazione"],
        )
    )

    return chart_mm & (chart_prob_line + chart_prob_points)

# precipitation - weekly
def precipitation_weekly_chart(df):
    chart_mm_week = (
        alt.Chart(df)
        .mark_bar(size=3, color="steelblue")
        .encode(
            x=alt.X("datetime:T", title="Data/Ora"),
            y="Precipitazioni (mm):Q",
            tooltip=["Data", "Ora", "Precipitazioni (mm)"],
        )
        .properties(title="precipitation and probability - week")
        .interactive()
    )

    chart_prob_week = (
        alt.Chart(df)
        .mark_line(color="orange")
        .encode(
            x=alt.X("datetime:T", title="Data/Ora"),
            y="Probabilità di Precipitazione:Q",
            tooltip=["Data", "Ora", "Probabilità di Precipitazione"],
        )
        .interactive()
    )

    return chart_mm_week & chart_prob_week

# humidity - daily
def humidity_daily_chart(df_oggi):
    chart_giornaliero = (
        alt.Chart(df_oggi)
        .mark_line(color="dodgerblue")
        .encode(
            x=alt.X("datetime:T", title="Ora", axis=alt.Axis(format="%H:%M")),
            y=alt.Y("Umidità (%):Q"),
            tooltip=["Ora", "Umidità (%)"],
        )
        .properties(title=f"relative humidity - {df_oggi['Data'].iloc[0]}")
        .interactive()
    )

    chart_giornaliero_punti = (
        alt.Chart(df_oggi)
        .mark_point(color="dodgerblue", filled=True, size=60)
        .encode(x="datetime:T", y="Umidità (%):Q", tooltip=["Ora", "Umidità (%)"])
    )

    return chart_giornaliero + chart_giornaliero_punti

# humidity - weekly
def humidity_weekly_chart(df):
    chart_settimanale = (
        alt.Chart(df)
        .mark_line(color="midnightblue")
        .encode(
            x="datetime:T",
            y="Umidità (%):Q",
            tooltip=["Data", "Ora", "Umidità (%)"],
        )
        .properties(title="relative humidity - week")
        .interactive()
    )
    return chart_settimanale

# wind - daily
def wind_daily_chart(df_oggi):
    # transforms the dataframe to track speed and gusts
    df_melted = df_oggi.melt(
        id_vars=["datetime"],
        value_vars=["Velocità Vento (km/h)", "Raffiche di Vento (km/h)"],
        var_name="Tipo",
        value_name="Valore",
    )

    chart_giornaliero = (
        alt.Chart(df_melted)
        .mark_line(point=True)
        .encode(
            x=alt.X("datetime:T", title="Ora", axis=alt.Axis(format="%H:%M")),
            y=alt.Y("Valore:Q", title="Vento (km/h)"),
            color=alt.Color(
                "Tipo:N",
                scale=alt.Scale(
                    domain=["Velocità Vento (km/h)", "Raffiche di Vento (km/h)"],
                    range=["green", "firebrick"],
                ),
            ),
            tooltip=["datetime:T", "Tipo:N", "Valore:Q"],
        )
        .properties(title=f"wind speed and gusts - {df_oggi['Data'].iloc[0]}")
        .interactive()
    )
    return chart_giornaliero

# wind - weekly
def wind_weekly_chart(df):
    # transforms the dataframe to track two curves
    df_melted_week = df.melt(
        id_vars=["datetime", "Data", "Ora"],
        value_vars=["Velocità Vento (km/h)", "Raffiche di Vento (km/h)"],
        var_name="Tipo",
        value_name="Valore",
    )

    chart_week = (
        alt.Chart(df_melted_week)
        .mark_line()
        .encode(
            x="datetime:T",
            y="Valore:Q",
            color=alt.Color(
                "Tipo:N",
                scale=alt.Scale(
                    domain=["Velocità Vento (km/h)", "Raffiche di Vento (km/h)"],
                    range=["green", "firebrick"],
                ),
            ),
            tooltip=["Data", "Ora", "Tipo", "Valore"],
        )
        .properties(title="wind speed and gusts - week")
        .interactive()
    )
    return chart_week