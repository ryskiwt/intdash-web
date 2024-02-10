import streamlit as st
import requests
from datetime import time, datetime, timezone

uuid = st.text_input("UUID")
name = st.text_input("計測名")
start_date = st.date_input("開始日時（日付）").astimezone(timezone.utc)
start_time = st.time_input("開始日時（時刻）", value=time(0, 0))
start_frac = st.number_input("開始日時（小数点以下）", min_value=0, max_value=999999999)
end_date = st.date_input("終了日時（日付）").astimezone(timezone.utc)
end_time = st.time_input("終了日時（時刻）", value=time(0, 0))
end_frac = st.number_input("終了日時（小数点以下）", min_value=0, max_value=999999999)

if st.button("検索する"):
    start_rfc3339 = datetime.combine(start_date, start_time).strftime(f'%Y-%m-%dT%H:%M:%S.{start_frac:09}Z')
    end_rfc3339 = datetime.combine(end_date, end_time).strftime(f'%Y-%m-%dT%H:%M:%S.{end_frac:09}Z')
    st.write(start_rfc3339)
    st.write(end_rfc3339)

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


