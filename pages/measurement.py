import streamlit as st
import requests

meas_uuid = None
if st.session_state.measurements_from_list:
    meas_uuid = st.session_state.measurements_meas_uuid = meas_uuid
    st.session_state.measurements_from_list = False
meas_uuid = st.text_input("計測UUID", value=meas_uuid)

params = {
    "name": meas_uuid
}
resp = requests.get(
    url=f"{st.session_state.url}/api/v1/projects/{st.session_state.project_uuid}/data_ids",
    headers={"X-Intdash-Token": st.session_state.token},
    params=params,
)
resp.raise_for_status()
resp = resp.json()

st.write(resp["items"])
