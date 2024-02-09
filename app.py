import streamlit as st
from streamlit-local-storage import LocalStorage
from streamlit_javascript import st_javascript

ls = LocalStorage() 

st.title("認証情報")

st.write(ls.getItem("url"))
st.write(ls.getItem("token"))
st.write(ls.getItem("project_uuid"))

url = st.text_input(label="intdashサーバーURL", placeholder="https://example.com")
token = st.text_input(label="APIトークン", type="password")
project_uuid = st.text_input("プロジェクトID")

if st.button("保存する"):
    ls.setItem("url", url)
    ls.setItem("token", token)
    ls.setItem("project_uuid", project_uuid)

    st.session_state["url"] = url
    st.session_state["token"] = token
    st.session_state["project_uuid"] = project_uuid

    st.write("local storage")
    st.write(ls.getItem("url"))
    st.write(ls.getItem("token"))
    st.write(ls.getItem("project_uuid"))

    st.write("session state")
    st.write(st.session_state["url"])
    st.write(st.session_state["token"])
    st.write(st.session_state["project_uuid"])

