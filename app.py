import streamlit as st
import requests

url = st.text_input("intdashサーバーURL", placeholder="https://example.com")
token = st.text_input("APIトークン", type="password")
node_id = st.text_input("ノードID")

if st.button("接続する"):
    resp = requests.get(
        url=f"{url}/api/auth/users/me",
        headers={"X-Intdash-Token": token},
    )
    resp.raise_for_status()
    st.write(resp.json())
