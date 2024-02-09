import streamlit as st
from streamlit_local_storage import LocalStorage

ls = LocalStorage() 

st.title("認証情報")

url = ls.getItem("url", key="get_item_url")
token = ls.getItem("token", key="get_item_token")
project_uuid = ls.getItem("project_uuid", key="get_item_project_uuid")

st.write(f"url: {url}")
st.write(f"token: {token}")
st.write(f"project_uuid: {project_uuid}")

url = st.text_input(label="intdashサーバーURL", placeholder="https://example.com", value=url)
token = st.text_input(label="APIトークン", type="password", value=token)
project_uuid = st.text_input("プロジェクトID", value=project_uuid)

if st.button("保存する"):
    ls.setItem("url", url)
    ls.setItem("token", token)
    ls.setItem("project_uuid", project_uuid)

    st.session_state["url"] = url
    st.session_state["token"] = token
    st.session_state["project_uuid"] = project_uuid

    st.write("session state")
    st.write(f"url: {url}")
    st.write(f"token: {token}")
    st.write(f"project_uuid: {project_uuid}")

