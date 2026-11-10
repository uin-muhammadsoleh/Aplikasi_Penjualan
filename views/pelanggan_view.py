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
                    "Nama Pelanggan": pel.get_nama(),
                    "Jumlah Riwayat Pesanan": len(pel.get_pesanan_list()),
                }
                for pel in semua_pelanggan
            ]
            st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada data pelanggan.")

    with tab_tambah:
        st.subheader("Tambah Pelanggan Baru")
        with st.form("form_tambah_pelanggan", clear_on_submit=False):
            nama_pel = st.text_input("Nama Lengkap Pelanggan *", placeholder="Contoh: Budi Santoso")
            # Peringatan error tepat di bawah textbox
            err_nama = st.empty()

            submit = st.form_submit_button("Simpan Pelanggan", type="primary")

            if submit:
                nama_clean = (nama_pel or "").strip()
                if not nama_clean or len(nama_clean) < 2:
                    err_nama.error("⚠️ Data input salah: Nama pelanggan wajib diisi (minimal 2 karakter).")
                elif len(nama_clean) > 100:
                    err_nama.error("⚠️ Data input salah: Nama pelanggan maksimal 100 karakter.")
                else:
                    try:
                        controller.tambah_pelanggan(nama_clean)
                        st.success(f"Pelanggan '{nama_clean}' berhasil ditambahkan!")
                        st.rerun()
                    except ValueError as err:
                        err_nama.error(f"⚠️ Data input tidak sesuai: {str(err)}")
                    except Exception as err:
                        st.error(f"Gagal menambahkan pelanggan: {err}")
