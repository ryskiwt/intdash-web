import streamlit as st
from streamlit_local_storage import LocalStorage

ls = LocalStorage() 

def ls_get(item_key, key=None):
    if item_key is None:
        return None

    item = ls.getItem(item_key, key=key if key is None else f"get_item_{item_key}")
    if (item is None) or ("storage" not in item) or (item["storage"] is None):
        return None

    return item["storage"]["value"]

def ls_set(item_key, item_value):
    ls.setItem(item_key, item_value)


st.title("認証情報")

url = ls_get("url")
token = ls_get("token")
project_uuid = ls_get("project_uuid")

st.write(f"url: {url}")
st.write(f"token: {token}")
st.write(f"project_uuid: {project_uuid}")

url = st.text_input(label="intdashサーバーURL", placeholder="https://example.com", value=url)
if url:
    ls_set("url", url)
    st.session_state["url"] = url

token = st.text_input(label="APIトークン", type="password", value=token)
if token:
    ls_set("token", token)
    st.session_state["token"] = token

project_uuid = st.text_input("プロジェクトID", value=project_uuid)
if project_uuid:
    ls_set("project_uuid", project_uuid)
    st.session_state["project_uuid"] = project_uuid

st.write("session state")
st.write(f"url: {url}")
st.write(f"token: {token}")
st.write(f"project_uuid: {project_uuid}")

