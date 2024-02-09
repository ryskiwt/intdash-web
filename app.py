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

st.write(f"url: {st.session_state.url}")
st.write(f"token: {st.session_state.token}")
st.write(f"project_uuid: {st.session_state.project_uuid}")


with st.form("creds_form"):
    url = st.text_input(label="intdashサーバーURL", placeholder="https://example.com", value=st.session_state.url)
    token = st.text_input(label="APIトークン", type="password", value=st.session_state.token)
    project_uuid = st.text_input(label="プロジェクトID", value=st.session_state.project_uuid)
    
    if st.form_submit_button("保存する"):
        st.session_state.url = url
        st.session_state.token = token
        st.session_state.project_uuid = project_uuid

        ls_set("url", url)
        ls_set("token", token)
        ls_set("project_uuid", project_uuid)


st.write("session state")
st.write(f"url: {st.session_state.url}")
st.write(f"token: {st.session_state.token}")
st.write(f"project_uuid: {st.session_state.project_uuid}")

