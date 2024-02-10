import streamlit as st
import requests
from datetime import time, datetime, timezone, timedelta
from zoneinfo import ZoneInfo
from urllib.parse import urlparse

with st.expander("検索条件", expanded=True):
    with st.container():
        col1, col2, col3 = st.columns(3)
        start_date = col1.date_input("開始日時（日付）")
        start_time = col2.time_input("開始日時（時刻）", value=time(0, 0))
        start_frac = col3.number_input("開始日時（小数点以下）", min_value=0, max_value=999999999)

    with st.container():
        col1, col2, col3 = st.columns(3)
        end_date = col1.date_input("終了日時（日付）")
        end_time = col2.time_input("終了日時（時刻）", value=time(0, 0))
        end_frac = col3.number_input("終了日時（小数点以下）", min_value=0, max_value=999999999)

    with st.container():
        col1, col2 = st.columns(2)
        name = col1.text_input("計測名")
        uuid = col2.text_input("UUID")

    tz = st.text_input("タイムゾーン", "Asia/Tokyo")
    page = st.number_input("ページ", value=1)
    search = st.button("検索する")

if search:
    params = {
        "start": datetime(
            start_date.year,
            start_date.month,
            start_date.day,
            start_time.hour,
            start_time.minute,
            start_time.second,
            tzinfo=ZoneInfo(tz),
        ).astimezone(timezone.utc).strftime(f'%Y-%m-%dT%H:%M:%S.{end_frac:09}Z'),
        "end": datetime(
            end_date.year,
            end_date.month,
            end_date.day,
            end_time.hour,
            end_time.minute,
            end_time.second,
            tzinfo=ZoneInfo(tz),
        ).astimezone(timezone.utc).strftime(f'%Y-%m-%dT%H:%M:%S.{end_frac:09}Z'),
        "page": page,
        "limit": 10,
    }
    if name is not None:
        params["name"] = name
    if uuid is not None:
        params["uuid"] = uuid

    resp = requests.get(
        url=f"{st.session_state.url}/api/v1/projects/{st.session_state.project_uuid}/measurements",
        headers={"X-Intdash-Token": st.session_state.token},
        params=params,
    )
    resp.raise_for_status()
    resp = resp.json()

    total_page = resp["page"]["total_count"]
    st.write(f"{page} / {total_page} pages")

    for item in resp["items"]:
        with st.container(border=True):
            meas_uuid = item["uuid"]
            duration = timedelta(microseconds=item["duration"])

            splitted = item["basetime"].split(".")
            start_time = datetime.fromisoformat(splitted[0]).astimezone(ZoneInfo(tz))
            end_time = start_time + duration

            st.write(start_time)
            st.write(end_time)

            hours = duration.seconds // 3600
            minutes = (duration.seconds - hours*3600) // 60
            seconds = duration.seconds - hours*3600 - minutes*60
            hours += duration.days*24

            st.write(f"{hours} 時間 {minutes} 分 {seconds} 秒")

            edge_uuid = item["edge_uuid"]
            resp = requests.get(
                url=f"{st.session_state.url}/api/auth/projects/{st.session_state.project_uuid}/edges/{edge_uuid}",
                headers={"X-Intdash-Token": st.session_state.token},
            )
            resp.raise_for_status()
            resp = resp.json()
            edge_name = resp["name"]
            st.write(f"{edge_name} ({edge_uuid})")

            st.write(f"{st.session_state.url}/console/measurements/{meas_uuid}/?projectUuid={st.session_state.project_uuid}")

            st.write(item)


parsed_url = urlparse(st.session_state.url)
st.sidebar.markdown("## 認証情報")
st.sidebar.markdown(f"**サーバー:** [{parsed_url.hostname}]({st.session_state.url}/console/projects/{st.session_state.project_uuid})")
st.sidebar.write("**プロジェクト:**", st.session_state.project_name)
st.sidebar.write("**ユーザー:**", st.session_state.user_display_name)