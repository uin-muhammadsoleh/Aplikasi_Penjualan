import streamlit as st

from controllers.auth_controller import AuthController
from controllers.produk_controller import ProdukController
from database.db import init_db
from views.produk_view import tampilkan_halaman_produk

st.set_page_config(page_title="Data Produk - Manajemen Produk MVC", page_icon="🛍️", layout="wide")
init_db()

auth_controller = AuthController()

# Proteksi halaman: Wajib login terlebih dahulu
if not auth_controller.is_logged_in():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {display: none !important;}
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.warning("⚠️ **Akses Ditolak**: Anda harus masuk (login) terlebih dahulu sebelum mengakses data produk.")
    if st.button("🔑 Menuju Halaman Login", type="primary"):
        st.switch_page("app.py")
    st.stop()

# Jika sudah login:
auth_controller.render_sidebar_user_info()

controller = ProdukController()
tampilkan_halaman_produk(controller)
