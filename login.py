import streamlit as st
import streamlit_authenticator as stauth

def to_plain_dict(obj):
    if hasattr(obj, "items"):
        return {k: to_plain_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_plain_dict(x) for x in obj]
    return obj

def get_authenticator():
    # 1. Cargar las credenciales y configuración desde los secretos
    credenciales = to_plain_dict(st.secrets["auth"]["credentials"])
    cookie_config = to_plain_dict(st.secrets["auth"]["cookie"])
    # pasword = credenciales["usernames"]["adrian"]["password"]
    # print(pasword)
    # hashed = stauth.Hasher().hash_passwords([pasword])
    # print(hashed)
    # hashed_password = stauth.Hasher.hash("MiPasswordSegura123")
    # print(hashed_password)
    
    # print(stauth.Hasher.generate(credenciales["usernames"]["adrian"]["password"]))

    return  stauth.Authenticate(
        credenciales,
        cookie_config["name"],
        cookie_config["key"],
        90,
        auto_hash=True,
    )
