import streamlit as st
import requests

url = st.text_input("intdashサーバーURL", placeholder="https://example.com")
token = st.text_input("APIトークン", type="password")
project_uuid = st.text_input("プロジェクトID")
node_id = st.text_input("ノードID")

if st.button("接続する"):
    resp = requests.get(
        url=f"{url}/api/v1/projects/{project_uuid}/measurements",
        headers={"X-Intdash-Token": token},
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


