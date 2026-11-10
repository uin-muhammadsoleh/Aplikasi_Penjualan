import pandas as pd
import streamlit as st
from controllers.pelanggan_controller import PelangganController


def tampilkan_halaman_pelanggan(controller: PelangganController):
    st.title("👥 Manajemen Pelanggan")
    st.caption(
        "Mengimplementasikan entitas **Pelanggan** dengan atribut `nama` "
        "dan method `lihat_produk()` (Relasi Association dengan Produk)."
    )

    tab_daftar, tab_tambah = st.tabs(["📋 Daftar Pelanggan", "➕ Tambah Pelanggan"])

    semua_pelanggan = controller.semua_pelanggan()

    with tab_daftar:
        st.subheader("Daftar Pelanggan Terdaftar")
        if semua_pelanggan:
            data = [
                {
                    "ID": pel.id,
                    "Nama Pelanggan": pel.nama,
                    "Jumlah Riwayat Pesanan": len(pel.pesanan_list),
                }
                for pel in semua_pelanggan
            ]
            st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada data pelanggan.")

    with tab_tambah:
        st.subheader("Tambah Pelanggan Baru")
        with st.form("form_tambah_pelanggan", clear_on_submit=True):
            nama_pel = st.text_input("Nama Lengkap Pelanggan *", placeholder="Contoh: Budi Santoso")
            submit = st.form_submit_button("Simpan Pelanggan", type="primary")

            if submit:
                try:
                    controller.tambah_pelanggan(nama_pel)
                    st.success(f"Pelanggan '{nama_pel}' berhasil ditambahkan!")
                    st.rerun()
                except Exception as err:
                    st.error(f"Gagal: {err}")
