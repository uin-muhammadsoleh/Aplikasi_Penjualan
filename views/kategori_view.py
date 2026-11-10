import pandas as pd
import streamlit as st
from controllers.kategori_controller import KategoriController


def _val(obj, attr, default=None):
    if hasattr(obj, f"get_{attr}") and callable(getattr(obj, f"get_{attr}")):
        try:
            return getattr(obj, f"get_{attr}")()
        except Exception:
            pass
    return getattr(obj, attr, default)


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
                prods = _val(k, "daftar_produk", [])
                jml_produk = len(prods)
                daftar_nama_produk = (
                    ", ".join([_val(p, "nama", "") for p in prods])
                    if jml_produk > 0
                    else "(Belum ada produk)"
                )
                data.append(
                    {
                        "ID": k.id,
                        "Nama Kategori": _val(k, "nama", ""),
                        "Jumlah Produk": f"{jml_produk} produk",
                        "Daftar Produk (daftar_produk)": daftar_nama_produk,
                    }
                )

            st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

            st.write("---")
            st.subheader("🗑️ Hapus Kategori")
            opsi_kat = {f"#{k.id} - {_val(k, 'nama', '')}": k.id for k in semua_kat}
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
        with st.form("form_tambah_kategori", clear_on_submit=False):
            nama_baru = st.text_input("Nama Kategori *", placeholder="Contoh: Elektronik, Pakaian, Makanan...")
            # Peringatan error tepat di bawah textbox
            err_nama = st.empty()
            submit = st.form_submit_button("Simpan Kategori", type="primary")

            if submit:
                nama_clean = (nama_baru or "").strip()
                if not nama_clean or len(nama_clean) < 2:
                    err_nama.error("⚠️ Data input salah: Nama kategori wajib diisi (minimal 2 karakter).")
                elif len(nama_clean) > 100:
                    err_nama.error("⚠️ Data input salah: Nama kategori maksimal 100 karakter.")
                else:
                    try:
                        controller.tambah_kategori(nama_clean)
                        st.success(f"Kategori '{nama_clean}' berhasil ditambahkan!")
                        st.rerun()
                    except ValueError as err:
                        err_nama.error(f"⚠️ Data input tidak sesuai: {err}")
                    except Exception as err:
                        st.error(f"Gagal: {err}")
