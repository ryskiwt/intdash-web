import streamlit as st
import requests
from datetime import time, datetime, timezone, timedelta
from zoneinfo import ZoneInfo
from urllib.parse import urlparse
import pytz

STATUS_MAP = {
    "ready": "計測準備中",
    "measuring": "計測中",
    "resending": "再送中",
    "finished": "完了",
    "completed": "完了",
}

EDGE_NAME_MAP = {}
page = 1
while True:
    params = {
        "page": page,
        "per_page": 200,
    }
    resp = requests.get(
        url=f"{st.session_state.url}/api/auth/projects/{st.session_state.project_uuid}/edges",
        headers={"X-Intdash-Token": st.session_state.token},
        params=params,
    )
    resp.raise_for_status()
    resp = resp.json()
    for item in resp["items"]:
        EDGE_NAME_MAP[item["edge_uuid"]] = item["name"]

    page += 1
    if not resp["page"]["next"]:
        break
EDGE_UUID_MAP = {v:k for k,v in EDGE_NAME_MAP.items()}


def declare_variable(name, default):
    if name not in st.session_state:
        st.session_state[name] = default

declare_variable("measurements", [])
declare_variable("total_page", 0)
declare_variable("checked_measurement_uuids", [])


def on_click_search(start_date, start_time, start_frac, end_date, end_time, end_frac, meas_name, meas_uuid, edge_uuid, page, limit):
    limit = 50
    params = {
        "start": datetime(
            start_date.year,
            start_date.month,
            start_date.day,
            start_time.hour,
            start_time.minute,
            start_time.second,
            tzinfo=ZoneInfo(tz),
        ).astimezone(timezone.utc).strftime(f'%Y-%m-%dT%H:%M:%S.{start_frac:09}Z'),
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
        "limit": limit,
    }
    if meas_name is not None:
        params["name"] = meas_name
    if meas_uuid is not None:
        params["uuid"] = meas_uuid
    if edge_uuid is not None:
        params["edge_uuid"] = edge_uuid

    resp = requests.get(
        url=f"{st.session_state.url}/api/v1/projects/{st.session_state.project_uuid}/measurements",
        headers={"X-Intdash-Token": st.session_state.token},
        params=params,
    )
    resp.raise_for_status()
    resp = resp.json()

    st.session_state.total_page = -((-resp["page"]["total_count"])//limit)
    st.session_state.measurements = resp["items"]


with st.expander("検索条件", expanded=True):
    def craete_datetime_input(label):
        with st.container():
            col1, col2, col3 = st.columns(3)
            d = col1.date_input(label=f"{label}（日付）")
            t = col2.time_input(label=f"{label}（時刻）", value=time(0, 0))
            f = col3.number_input(label=f"{label}（小数点以下）", min_value=0, max_value=999999999)
        return d, t, f

    start_date, start_time, start_frac = craete_datetime_input(label="開始日時")
    end_date, end_time, end_frac = craete_datetime_input(label="終了日時")

    with st.container():
        col1, col2 = st.columns(2)
        meas_name = col1.text_input(label="計測名", placeholder="Optional")
        meas_uuid = col2.text_input(label="UUID", placeholder="Optional")
    
    edge_name_q = st.selectbox(
        label="エッジ名",
        options=[{"name": v, "uuid": k} for k,v in EDGE_NAME_MAP.items()],
        format_func=lambda item: item["name"],
        index=None,
    )
    
    tz = st.selectbox(
        label="タイムゾーン",
        options=pytz.common_timezones,
        index=pytz.common_timezones.index("Asia/Tokyo"),
    )

    with st.container():
        col1, col2 = st.columns(2)
        page = col1.number_input("ページ", value=1, min_value=1)
        limit = col2.number_input("件数/ページ", value=50, min_value=1)

    st.button("検索する", on_click=on_click_search, kwargs={
        "start_date": start_date, 
        "start_time": start_time, 
        "start_frac": start_frac, 
        "end_date": end_date, 
        "end_time": end_time, 
        "end_frac": end_frac, 
        "meas_name": meas_name, 
        "meas_uuid": meas_uuid, 
        "edge_uuid": None if edge_name_q is None else edge_name_q["uuid"], 
        "page": page,
        "limit": limit, 
    })

def td_to_human_readable_string(td):
    hours = td.seconds // 3600
    minutes = (td.seconds - hours*3600) // 60
    seconds = td.seconds - hours*3600 - minutes*60
    hours += td.days*24
    return f"{hours} 時間 {minutes} 分 {seconds} 秒"

def cropped_start_end(basetime, duration, tz):
    splitted = basetime.split(".")
    start_time = datetime.fromisoformat(splitted[0]).astimezone(ZoneInfo(tz))
    end_time = (start_time + duration).replace(microseconds=0)
    return start_time, end_time

with st.expander("検索結果", expanded=True):
    st.write(f"{page} / {st.session_state.total_page} pages")

    for i, item in enumerate(st.session_state.measurements):
        with st.container(border=True):
            meas_uuid = item["uuid"]
            meas_name = "<名称なし>" if item["name"]=="" else item["name"]
            edge_uuid = item["edge_uuid"]
            edge_name = EDGE_NAME_MAP[edge_uuid]

            with st.container():
                duration = timedelta(microseconds=item["max_elapsed_time"])
                start_time, end_time = cropped_start_end(item["basetime"], duration, tz)

                col1, col2 = st.columns(2)
                col1.write(start_time.strftime("%Y/%m/%d %H:%M:%S") + " - " + end_time.strftime("%Y/%m/%d %H:%M:%S"))
                col2.write(td_to_human_readable_string(duration))

            with st.container():
                col1, col2 = st.columns(2)
                col1.write("ステータス: " + STATUS_MAP[item["sequences"]["status"]])

                received_chunks_ratio = item["sequences"]["received_chunks_ratio"] * 100.0
                received_data_points = item["sequences"]["received_data_points"]
                expected_data_points = item["sequences"]["expected_data_points"]
                processed_ratio = item["processed_ratio"] * 100.0

                if received_data_points <= expected_data_points:
                    col2.write(f"{received_chunks_ratio:3.1f} % ({received_data_points} / {expected_data_points} points)")
                else:
                    col2.write(f"{processed_ratio:3.1f} % (iSCPv1)")

            st.write(f"エッジ名: [{edge_name}]({st.session_state.url}/console/edges/{edge_uuid}/?projectUuid={st.session_state.project_uuid})  ({edge_uuid})")
            st.write(f"計測名: [{meas_name}]({st.session_state.url}/console/measurements/{meas_uuid}/?projectUuid={st.session_state.project_uuid}) ({meas_uuid})")

            checked = meas_uuid in st.session_state.checked_measurement_uuids
            if st.checkbox("この計測を対象にする", key=f"checkbox_{i}", value=checked):
                st.session_state.checked_measurement_uuids.add(meas_uuid)
            else:
                if checked:
                    st.session_state.checked_measurement_uuids.remove(meas_uuid)

st.write(st.session_state.checked_measurement_uuids)





parsed_url = urlparse(st.session_state.url)
st.sidebar.markdown("## 認証情報")
st.sidebar.markdown(f"**サーバー:** [{parsed_url.hostname}]({st.session_state.url}/console/projects/{st.session_state.project_uuid})")
st.sidebar.write("**プロジェクト:**", st.session_state.project_name)
st.sidebar.write("**ユーザー:**", st.session_state.user_display_name)