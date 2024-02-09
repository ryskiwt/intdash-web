import streamlit as st
from streamlit_local_storage import LocalStorage

ls = LocalStorage() 

def ls_get(item_key, key=None):
    if item_key is None:
        return None

    item = ls.getItem(item_key, key=f"get_item_{item_key}" if (key is None) else key)
    if (item is None) or ("storage" not in item) or (item["storage"] is None):
        return None

    return item["storage"]["value"]

def ls_set(item_key, item_value, key=None):
    ls.setItem(item_key, item_value, key=f"set_item_{item_key}" if (key is None) else key)


st.title("認証情報")

if ("url" not in st.session_state) or (st.session_state.url is None):
    st.session_state.url = ls_get("url")
if ("token" not in st.session_state) or (st.session_state.token is None):
    st.session_state.token = ls_get("token")
if ("project_uuid" not in st.session_state) or (st.session_state.project_uuid is None):
    st.session_state.project_uuid = ls_get("project_uuid")

url = st.text_input(label="intdashサーバーURL", placeholder="https://example.com", value=st.session_state.url)
token = st.text_input(label="APIトークン", type="password", value=st.session_state.token)
project_uuid = st.text_input(label="プロジェクトID", value=st.session_state.project_uuid)


if url:
    st.session_state.url = url
    ls_set("url", url)
if token:
    st.session_state.token = token
    ls_set("token", token)
if project_uuid:
    st.session_state.project_uuid = project_uuid
    ls_set("project_uuid", project_uuid)
