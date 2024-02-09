import streamlit as st
from streamlit_javascript import st_javascript

def get_from_ls(k):
    return st_javascript(f"localStorage.getItem('{k}') || '';")

def set_to_ls(k, v):
    st_javascript(f"localStorage.setItem('{k}', '{v}');")

st.title("認証情報")

st.write(get_from_ls("url"))
st.write(get_from_ls("token"))
st.write(get_from_ls("project_uuid"))

url = st.text_input(label="intdashサーバーURL", placeholder="https://example.com")
token = st.text_input(label="APIトークン", type="password")
project_uuid = st.text_input("プロジェクトID")

if st.button("保存する"):
    set_to_ls("url", url)
    set_to_ls("token", token)
    set_to_ls("project_uuid", project_uuid)

    st.session_state["url"] = url
    st.session_state["token"] = token
    st.session_state["project_uuid"] = project_uuid

    st.write("local storage")
    st.write(get_from_ls("url"))
    st.write(get_from_ls("token"))
    st.write(get_from_ls("project_uuid"))

    st.write("session state")
    st.write(st.session_state["url"])
    st.write(st.session_state["token"])
    st.write(st.session_state["project_uuid"])

