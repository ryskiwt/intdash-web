import streamlit as st
import requests

query_params = st.query_params.to_dict()
meas_uuid = query_params["uuid"]

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
