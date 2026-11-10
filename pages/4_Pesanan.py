import streamlit as st
from controllers.auth_controller import AuthController
from controllers.pelanggan_controller import PelangganController
from controllers.pesanan_controller import PesananController
from controllers.produk_controller import ProdukController
from database.db import init_db
from views.pesanan_view import tampilkan_halaman_pesanan

st.set_page_config(page_title="Pesanan & Transaksi - MVC", page_icon="🏷️", layout="wide")
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

pesanan_ctrl = PesananController()
produk_ctrl = ProdukController()
pelanggan_ctrl = PelangganController()

tampilkan_halaman_pesanan(pesanan_ctrl, produk_ctrl, pelanggan_ctrl)
