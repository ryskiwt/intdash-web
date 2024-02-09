import streamlit as st
import requests

st.text_input("UUID")
st.text_input("計測名")
st.date_input("開始日時（日付）")
st.time_input("開始日時（時刻）", value=None)
st.number_input("開始日時（小数点以下）", min_value=0, max_value=999999999)
st.date_input("終了日時（日付）")
st.time_input("終了日時（時刻）", value=None)
st.number_input("終了日時（小数点以下）", min_value=0, max_value=999999999)

if st.button("検索する"):
    
    resp = requests.get(
        url=f"{url}/api/v1/projects/{st.session_state.project_uuid}/measurements",
        headers={"X-Intdash-Token": token},
        params={
            "start": project_uuid,
            "end": project_uuid,
            "name": project_uuid,
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


