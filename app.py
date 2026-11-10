import streamlit as st
from controllers.auth_controller import AuthController
from controllers.kategori_controller import KategoriController
from controllers.pelanggan_controller import PelangganController
from controllers.pesanan_controller import PesananController
from controllers.produk_controller import ProdukController
from database.db import get_database_info, init_db
from views.auth_view import tampilkan_halaman_auth

st.set_page_config(
    page_title="Sistem Manajemen Produk & Penjualan - MVC",
    page_icon="📦",
    layout="wide",
)
init_db()

auth_controller = AuthController()

# Cek status login pengguna
if not auth_controller.is_logged_in():
    # Sembunyikan navigasi halaman di sidebar untuk pengguna yang belum login
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {display: none !important;}
        </style>
        """,
        unsafe_allow_html=True,
    )
    tampilkan_halaman_auth(auth_controller)
else:
    # Tampilkan informasi profil dan tombol logout di sidebar
    auth_controller.render_sidebar_user_info()

    user = auth_controller.get_current_user()
    nama = user["nama_lengkap"] if user else "Pengguna"

    st.title("📦 Sistem Manajemen Produk & Transaksi")
    st.markdown(f"### Selamat datang kembali, **{nama}**! 👋")
    st.write(
        "Aplikasi ini mengimplementasikan pola arsitektur **MVC (Model–View–Controller)** "
        "yang disesuaikan dengan **Rancangan Class Diagram Studi Kasus** (Produk, Kategori, Pelanggan, Pesanan, DetailPesanan)."
    )

    st.write("---")

    # Ambil data ringkasan dari masing-masing Controller
    produk_ctrl = ProdukController()
    kategori_ctrl = KategoriController()
    pelanggan_ctrl = PelangganController()
    pesanan_ctrl = PesananController()

    daftar_produk = produk_ctrl.semua_produk()
    daftar_kategori = kategori_ctrl.semua_kategori()
    daftar_pelanggan = pelanggan_ctrl.semua_pelanggan()
    daftar_pesanan = pesanan_ctrl.semua_pesanan()

    # Ringkasan Statistik 4 Entitas
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📦 Total Produk", f"{len(daftar_produk)} produk")
    c2.metric("🗂️ Total Kategori", f"{len(daftar_kategori)} kategori")
    c3.metric("👥 Total Pelanggan", f"{len(daftar_pelanggan)} orang")
    c4.metric("🏷️ Total Pesanan", f"{len(daftar_pesanan)} transaksi")

    st.write("")
    st.subheader("🚀 Pintasan Menu Utama:")
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        if st.button("🛍️ Menu Produk", use_container_width=True, type="primary"):
            st.session_state["produk_mode"] = "daftar"
            st.switch_page("pages/1_Produk.py")
    with b2:
        if st.button("🗂️ Menu Kategori", use_container_width=True):
            st.switch_page("pages/2_Kategori.py")
    with b3:
        if st.button("👥 Menu Pelanggan", use_container_width=True):
            st.switch_page("pages/3_Pelanggan.py")
    with b4:
        if st.button("🏷️ Menu Pesanan", use_container_width=True):
            st.switch_page("pages/4_Pesanan.py")

    st.write("---")
    st.markdown("""
    #### 📐 Pemetaan Class Diagram Studi Kasus:
    1. **`Produk`**: Atribut `nama`, `harga`, method `get_info()`, serta relasi *Aggregation* ke **`Kategori`** dan *Association* ke **`Pelanggan`**.
    2. **`Kategori`**: Atribut `nama`, relasi koleksi `daftar_produk`, dan method `tambah_produk()`.
    3. **`Pelanggan`**: Atribut `nama`, dan method `lihat_produk()`.
    4. **`Pesanan`**: Atribut `nomor`, koleksi `detail`, dan method `tambah_produk()`.
    5. **`DetailPesanan`**: Relasi *Composition* dengan **`Pesanan`**, atribut `produk`, `jumlah`, dan method `get_total()`.
    """)

    info = get_database_info()
    st.success(f"🟢 Database aktif: **{info}**")
