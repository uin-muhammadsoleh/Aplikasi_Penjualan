import pandas as pd
import streamlit as st
from controllers.kategori_controller import KategoriController


def tampilkan_halaman_kategori(controller: KategoriController):
    st.title("🗂️ Manajemen Kategori")
    st.caption(
        "Mengimplementasikan entitas **Kategori** dengan atribut `nama`, `daftar_produk`, "
        "dan method `tambah_produk()` (Relasi Aggregation dengan Produk)."
    )

    tab_daftar, tab_tambah = st.tabs(["📋 Daftar Kategori", "➕ Tambah Kategori"])

    semua_kat = controller.semua_kategori()

    with tab_daftar:
        st.subheader("Daftar Kategori Produk")
        if semua_kat:
            data = []
            for k in semua_kat:
                jml_produk = len(k.daftar_produk)
                daftar_nama_produk = (
                    ", ".join([p.nama for p in k.daftar_produk])
                    if jml_produk > 0
                    else "(Belum ada produk)"
                )
                data.append(
                    {
                        "ID": k.id,
                        "Nama Kategori": k.nama,
                        "Jumlah Produk": f"{jml_produk} produk",
                        "Daftar Produk (daftar_produk)": daftar_nama_produk,
                    }
                )

            st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

            st.write("---")
            st.subheader("🗑️ Hapus Kategori")
            opsi_kat = {f"#{k.id} - {k.nama}": k.id for k in semua_kat}
            terpilih = st.selectbox("Pilih kategori yang ingin dihapus:", options=list(opsi_kat.keys()))
            if st.button("Hapus Kategori", type="secondary"):
                try:
                    controller.hapus_kategori(opsi_kat[terpilih])
                    st.success("Kategori berhasil dihapus.")
                    st.rerun()
                except Exception as err:
                    st.error(f"Gagal menghapus: {err}")
        else:
            st.info("Belum ada kategori yang terdaftar.")

    with tab_tambah:
        st.subheader("Tambah Kategori Baru")
        with st.form("form_tambah_kategori", clear_on_submit=True):
            nama_baru = st.text_input("Nama Kategori *", placeholder="Contoh: Elektronik, Pakaian, Makanan...")
            submit = st.form_submit_button("Simpan Kategori", type="primary")

            if submit:
                try:
                    controller.tambah_kategori(nama_baru)
                    st.success(f"Kategori '{nama_baru}' berhasil ditambahkan!")
                    st.rerun()
                except Exception as err:
                    st.error(f"Gagal: {err}")
