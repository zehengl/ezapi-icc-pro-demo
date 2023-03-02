import io
from datetime import date, time

import pandas as pd
import streamlit as st
from icc_pro import ICC_PRO


def make_datetime_str(date, time):
    return "".join(
        [
            f"{date.year}",
            f"{date.month}".zfill(2),
            f"{date.day}".zfill(2),
            f"{time.hour}".zfill(2),
            f"{time.minute}".zfill(2),
            f"{time.second}".zfill(2),
        ]
    )


def make_excel(df):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer) as writer:
        df.to_excel(writer, index=False)
    return buffer


st.set_page_config(page_title="parks-irrigation", page_icon=":national_park:")
_, center, _ = st.columns([2, 1, 2])
with center:
    st.image(
        "https://cdn0.iconfinder.com/data/icons/citycons/150/Citycons_park-512.png",
        use_column_width=True,
    )
st.title("parks-irrigation")
st.caption("A study on parks irrigation data")

use_default = st.checkbox("Use default secrets")

if not use_default:
    secrets = {}
    secrets["host"] = st.text_input("Host", type="password")
    secrets["username"] = st.text_input("Username", type="password")
    secrets["password"] = st.text_input("Password", type="password")
    secrets["client_id"] = st.text_input("Client ID", type="password")
    secrets["client_secret"] = st.text_input("Client Secret", type="password")
    if (
        not secrets["host"]
        or not secrets["username"]
        or not secrets["password"]
        or not secrets["client_id"]
        or not secrets["client_secret"]
    ):
        st.stop()
else:
    if (
        not st.secrets.get("host")
        or not st.secrets.get("username")
        or not st.secrets.get("password")
        or not st.secrets.get("client_id")
        or not st.secrets.get("client_secret")
    ):
        st.error("Default Secrets not configured properly")
        st.stop()
    secrets = st.secrets

try:
    iccpro = ICC_PRO(**secrets)
except:
    st.error("Something wrong with secrets")
    st.stop()

st.subheader("Valves General Info")
valves_general_info = iccpro.get_valves_general_info()
df = pd.DataFrame(valves_general_info)
st.dataframe(df, use_container_width=True)
st.download_button(
    "Download Valves General Info",
    make_excel(df),
    "valves_general_info.xlsx",
    "text/csv",
)

st.subheader("Valves GIS Info")
valves_gis_info = iccpro.get_valves_gis_info()
df = pd.DataFrame(valves_gis_info)
st.dataframe(df, use_container_width=True)
st.download_button(
    "Download Valves GIS Info",
    make_excel(df),
    "valves_gis_info.xlsx",
    "text/csv",
)

st.subheader("Valves Status")
resp = iccpro.get_valves_status()
valves_status = resp["status"]
last_update = resp["LastUpdate"]
st.caption(f"Last Update at {last_update}")
df = pd.DataFrame(valves_status)
st.dataframe(df, use_container_width=True)
st.download_button(
    "Download Valves Status",
    make_excel(df),
    f"valves_status.xlsx",
    "text/csv",
)

st.subheader("Meters General Info")
meters_general_info = iccpro.get_meters_general_info()
df = pd.DataFrame(meters_general_info)
st.dataframe(df, use_container_width=True)
st.download_button(
    "Download Meters General Info",
    make_excel(df),
    "meters_general_info.xlsx",
    "text/csv",
)

st.subheader("Virtual Meters General Info")
virtual_meters_general_info = iccpro.get_virtual_meters_general_info()
df = pd.DataFrame(virtual_meters_general_info)
st.dataframe(df, use_container_width=True)
st.download_button(
    "Download Meters General Info",
    make_excel(df),
    "virtual_meters_general_info.xlsx",
    "text/csv",
)

st.subheader("Programs General Info")
programs_general_info = iccpro.get_programs_general_info()
df = pd.DataFrame(programs_general_info)
st.dataframe(df, use_container_width=True)
st.download_button(
    "Download Programs General Info",
    make_excel(df),
    "programs_general_info.xlsx",
    "text/csv",
)

st.subheader("Programs Detailed Info")
programs_detailed_info = iccpro.get_programs_detailed_info()
df = pd.DataFrame(programs_detailed_info)
st.dataframe(df, use_container_width=True)
st.download_button(
    "Download Programs Detailed Info",
    make_excel(df),
    "programs_detailed_info.xlsx",
    "text/csv",
)

st.subheader("Analog Inputs General Info")
analog_inputs_general_info = iccpro.get_analog_inputs_general_info()
df = pd.DataFrame(analog_inputs_general_info)
st.dataframe(df, use_container_width=True)
st.download_button(
    "Download Analog Inputs General Info",
    make_excel(df),
    "analog_inputs_general_info.xlsx",
    "text/csv",
)


st.subheader("Analog Inputs Current Data")
resp = iccpro.get_analog_inputs_current_data()
analog_inputs_current_data = resp["Data"]
df = pd.DataFrame(analog_inputs_current_data)
st.dataframe(df, use_container_width=True)
st.download_button(
    "Download Analog Inputs Current Data",
    make_excel(df),
    "analog_inputs_current_data.xlsx",
    "text/csv",
)

st.subheader("Analog Inputs Historical Data")
st.caption("Weekly data")

label, left, right = st.columns([1, 2, 2])
with label:
    st.text_input("", "From", disabled=True, key="from_analog_inputs")
with left:
    fromdate = st.date_input("Date", date(2022, 1, 1), key="fromdate_analog_inputs")
with right:
    fromtime = st.time_input("Time", time(0, 0), key="fromtime_analog_inputs")

fromdatetime = make_datetime_str(fromdate, fromtime)

label, left, right = st.columns([1, 2, 2])
with label:
    st.text_input("", "To", disabled=True, key="to_analog_inputs")
with left:
    todate = st.date_input("Date", date(2022, 12, 31), key="todate_analog_inputs")
with right:
    totime = st.time_input("Time", time(23, 59), key="totime_analog_inputs")

todatetime = make_datetime_str(todate, totime)

resp = iccpro.get_analog_inputs_historical_data(
    fromdatetime=fromdatetime, todatetime=todatetime, resolution=3
)
dfs = []
for item in resp["Data"]:
    _df = pd.DataFrame(item["Data"])
    _df["Time"] = item["Time"]
    dfs.append(_df)
df = pd.concat(dfs, ignore_index=True)
st.dataframe(df, use_container_width=True)
st.download_button(
    "Download Analog Inputs Historical Data",
    make_excel(df),
    "analog_inputs_historical_data.xlsx",
    "text/csv",
)


st.subheader("Sensors General Info")
sensors_general_info = iccpro.get_sensors_general_info()
df = pd.DataFrame(sensors_general_info)
st.dataframe(df, use_container_width=True)
st.download_button(
    "Download Sensors General Info",
    make_excel(df),
    "sensors_general_info.xlsx",
    "text/csv",
)


st.subheader("Sensors Current Data")
resp = iccpro.get_sensors_current_data()
sensors_current_data = resp["Data"]
df = pd.DataFrame(sensors_current_data)
st.dataframe(df, use_container_width=True)
st.download_button(
    "Download Sensors Current Data",
    make_excel(df),
    "sensors_current_data.xlsx",
    "text/csv",
)

st.subheader("Sensors Historical Data")
st.caption("Weekly data")

label, left, right = st.columns([1, 2, 2])
with label:
    st.text_input("", "From", disabled=True, key="from_sensors")
with left:
    fromdate = st.date_input("Date", date(2022, 1, 1), key="fromdate_sensors")
with right:
    fromtime = st.time_input("Time", time(0, 0), key="fromtime_sensors")

fromdatetime = make_datetime_str(fromdate, fromtime)

label, left, right = st.columns([1, 2, 2])
with label:
    st.text_input("", "To", disabled=True, key="to_sensors")
with left:
    todate = st.date_input("Date", date(2022, 12, 31), key="todate_sensors")
with right:
    totime = st.time_input("Time", time(23, 59), key="totime_sensors")

todatetime = make_datetime_str(fromdate, fromtime)

resp = iccpro.get_sensors_historical_data(
    fromdatetime=fromdatetime, todatetime=todatetime, resolution=3
)
dfs = []
for item in resp["Data"]:
    _df = pd.DataFrame(item["Data"])
    _df["Time"] = item["Time"]
    dfs.append(_df)
df = pd.concat(dfs, ignore_index=True)
st.dataframe(df, use_container_width=True)
st.download_button(
    "Download Sensors Historical Data",
    make_excel(df),
    "sensors_historical_data.xlsx",
    "text/csv",
)

# st.subheader("Meters Historical Accumulations")
# st.caption("2022 monthly data")
# resp = iccpro.get_meters_historical_accumulations(
#     fromdatetime="20220101000000", todatetime="20221231235959", resolution=4
# )
# dfs = []
# for item in resp["Data"]:
#     _df = pd.DataFrame(item["Data"])
#     _df["Time"] = item["Time"]
#     dfs.append(_df)
# df = pd.concat(dfs, ignore_index=True)
# st.dataframe(df, use_container_width=True)
# st.download_button(
#     "Download Meters Historical Accumulations",
#     make_excel(df),
#     "meters_historical_accumulations.xlsx",
#     "text/csv",
# )

# st.subheader("Valves Historical Accumulations")
# st.caption("2022 monthly data")
# resp = iccpro.get_valves_historical_accumulations(
#     fromdatetime="20220101000000", todatetime="20221231235959", resolution=4
# )
# dfs = []
# for item in resp["Data"]:
#     _df = pd.DataFrame(item["Data"])
#     _df["Time"] = item["Time"]
#     dfs.append(_df)
# df = pd.concat(dfs, ignore_index=True)
# st.dataframe(df, use_container_width=True)
# st.download_button(
#     "Download Valves Historical Accumulations",
#     make_excel(df),
#     "valves_historical_accumulations.xlsx",
#     "text/csv",
# )
