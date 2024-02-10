import streamlit as st
import requests
from datetime import time, datetime, timezone
from zoneinfo import ZoneInfo

with st.expander("検索条件", expanded=True):
    with st.container():
        col1, col2 = st.columns(2)
        name = col1.text_input("計測名")
        uuid = col2.text_input("UUID")

    with st.container()
        col1, col2, col3 = st.columns(3)
        start_date = col1.date_input("開始日時（日付）")
        start_time = col2.time_input("開始日時（時刻）", value=time(0, 0))
        start_frac = col3.number_input("開始日時（小数点以下）", min_value=0, max_value=999999999)

    with st.container()
        col1, col2, col3 = st.columns(3)
        end_date = col1.date_input("終了日時（日付）")
        end_time = col2.time_input("終了日時（時刻）", value=time(0, 0))
        end_frac = col3.number_input("終了日時（小数点以下）", min_value=0, max_value=999999999)

    tz = st.text_input("タイムゾーン", "Asia/Tokyo")

start_rfc3339 = datetime(
    start_date.year,
    start_date.month,
    start_date.day,
    start_time.hour,
    start_time.minute,
    start_time.second,
    tzinfo=ZoneInfo(tz),
).astimezone(timezone.utc).strftime(f'%Y-%m-%dT%H:%M:%S.{end_frac:09}Z')

end_rfc3339 = datetime(
    end_date.year,
    end_date.month,
    end_date.day,
    end_time.hour,
    end_time.minute,
    end_time.second,
    tzinfo=ZoneInfo(tz),
).astimezone(timezone.utc).strftime(f'%Y-%m-%dT%H:%M:%S.{end_frac:09}Z')

if st.button("検索する"):

    resp = requests.get(
        url=f"{url}/api/v1/projects/{st.session_state.project_uuid}/measurements",
        headers={"X-Intdash-Token": token},
        params={
            "uuid": uuid,
            "name": name,
            "start": start_rfc3339,
            "end": end_rfc3339,
        }
    )
    resp.raise_for_status()
    items = resp.json()

    for item in items:
        container = st.container(border=True)
        with container:
            st.write(item["name"])
            st.write(item["uuid"])
            st.write(item["base_time"])
            st.write(item["duration"])
            st.write(item["edge_uuid"])
            st.write(item)


