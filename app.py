import streamlit as st
from streamlit_javascript import st_javascript

def get_from_ls(k):
    return st_javascript(f"localStorage.getItem('{k}');")

def set_to_ls(k, v):
    st_javascript(f"localStorage.setItem('{k}', '{v}');")

st.title("認証情報")

url = st.text_input(label="intdashサーバーURL", placeholder="https://example.com", value=get_from_ls("url"))
token = st.text_input(label="APIトークン", type="password", value=get_from_ls("token"))
project_uuid = st.text_input("プロジェクトID", value=get_from_ls("project_uuid"))

if st.button("保存する"):
    set_to_ls("url", url)
    set_to_ls("token", token)
    set_to_ls("project_uuid", project_uuid)

    st.session_state["url"] = url
    st.session_state["token"] = token
    st.session_state["project_uuid"] = project_uuid
