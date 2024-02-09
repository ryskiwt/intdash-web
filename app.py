import streamlit as st
from streamlit_javascript import st_javascript
import requests

def get_from_local_storage(k):
    return st_javascript(
        f"localStorage.getItem('{k}');"
    )

def set_to_local_storage(k, v):
    st_javascript(
        f"localStorage.setItem('{k}', {v});"
    )

url = st.text_input("intdashサーバーURL", placeholder="https://example.com")
token = st.text_input("APIトークン", type="password")
project_uuid = st.text_input("プロジェクトID")
node_id = st.text_input("ノードID")


if st.button("接続する"):
    resp = requests.get(
        url=f"{url}/api/v1/projects/{project_uuid}/measurements",
        headers={"X-Intdash-Token": token},
        params={
            "project_uuid": project_uuid,
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


