import streamlit as st
from streamlit_local_storage import LocalStorage
import requests

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

if ("url" not in st.session_state) or (st.session_state.url is None):
    st.session_state.url = ls_get("url")
if ("token" not in st.session_state) or (st.session_state.token is None):
    st.session_state.token = ls_get("token")
if ("project_uuid" not in st.session_state) or (st.session_state.project_uuid is None):
    st.session_state.project_uuid = ls_get("project_uuid")
if ("project_name" not in st.session_state) or (st.session_state.project_uuid is None):
    st.session_state.project_name = ls_get("project_name")

st.header("認証情報", divider=True)

url = st.text_input(label="intdashサーバーURL", placeholder="https://example.com", value=st.session_state.url)
token = st.text_input(label="APIトークン", type="password", value=st.session_state.token)
project_uuid = st.text_input(label="プロジェクトID", placeholder="00000000-0000-0000-0000-000000000000", value=st.session_state.project_uuid)

st.session_state.url = url
st.session_state.token = token
st.session_state.project_uuid = project_uuid
ls_set("url", url)
ls_set("token", token)
ls_set("project_uuid", project_uuid)

try:
    resp = requests.get(
        url=f"{url}/api/auth/projects/{project_uuid}",
        headers={"X-Intdash-Token": token},
    )
    resp.raise_for_status()
    project_name = resp.json()["name"]

    st.session_state.project_name = project_name
    ls_set("project_name", project_name)

except Exception as e:
    st.error(f"入力に誤りがあります。: {e}")

masked_token = None if st.session_state.token is None else "*****"
st.sidebar.markdown("# 認証情報")
st.sidebar.markdown(f"- **サーバーURL**: {st.session_state.url}")
st.sidebar.markdown(f"- **APIトークン**: {masked_token}")
st.sidebar.markdown(f"- **プロジェクト**: {st.session_state.project_name}")