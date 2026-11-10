import streamlit as st
from controllers.auth_controller import AuthController
from controllers.kategori_controller import KategoriController
from database.db import init_db
from views.kategori_view import tampilkan_halaman_kategori

st.set_page_config(page_title="Kategori Produk - MVC", page_icon="🗂️", layout="wide")
init_db()

auth_controller = AuthController()

if not auth_controller.is_logged_in():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {display: none !important;}
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.warning("⚠️ **Akses Ditolak**: Anda harus login terlebih dahulu.")
    if st.button("🔑 Menuju Halaman Login", type="primary"):
        st.switch_page("app.py")
    st.stop()

auth_controller.render_sidebar_user_info()

controller = KategoriController()
tampilkan_halaman_kategori(controller)
