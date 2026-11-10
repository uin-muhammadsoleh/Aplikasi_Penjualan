import streamlit as st


@st.dialog("Konfirmasi Hapus Produk")
def konfirmasi_hapus_dialog(produk_id: int, nama_produk: str, controller):
    """Pop-up modal untuk mengonfirmasi penghapusan produk."""
    st.markdown("### ⚠️ Konfirmasi Penghapusan")
    st.write(f"Apakah Anda yakin ingin menghapus produk **{nama_produk}** (ID: `#{produk_id}`)?")
    st.warning("Tindakan ini permanen dan data produk tidak dapat dikembalikan.")

    col_hapus, col_batal = st.columns(2)
    with col_hapus:
        if st.button("🗑️ Ya, Hapus Produk", type="primary", use_container_width=True):
            try:
                controller.hapus_produk(produk_id)
                st.session_state["flash_message"] = {
                    "type": "success",
                    "text": f"Produk '{nama_produk}' berhasil dihapus dari database.",
                }
                st.rerun()
            except Exception as e:
                st.error(f"Gagal menghapus produk: {str(e)}")
    with col_batal:
        if st.button("❌ Batal", use_container_width=True):
            st.rerun()


def tampilkan_halaman_produk(controller):
    """Menampilkan antarmuka manajemen produk dengan daftar tabel, tombol tambah di atas,
    tombol edit & hapus di setiap baris, serta dialog modal untuk konfirmasi hapus.
    """
    if "produk_mode" not in st.session_state:
        st.session_state["produk_mode"] = "daftar"

    # Tampilkan notifikasi flash jika ada
    if "flash_message" in st.session_state:
        flash = st.session_state.pop("flash_message")
        if flash.get("type") == "success":
            st.success(f"✅ {flash.get('text')}")
        elif flash.get("type") == "error":
            st.error(f"❌ {flash.get('text')}")

    mode = st.session_state["produk_mode"]
    daftar_kategori = controller.semua_kategori()

    # ==============================================================
    # 1. HALAMAN TAMBAH PRODUK
    # ==============================================================
    if mode == "tambah":
        if st.button("⬅️ Kembali ke Daftar Produk"):
            st.session_state["produk_mode"] = "daftar"
            st.rerun()

        st.title("➕ Tambah Produk Baru")
        st.caption("Tambahkan produk baru dengan menentukan Kategori (Aggregation sesuai Class Diagram).")

        with st.form("form_tambah_produk", clear_on_submit=False):
            nama_produk = st.text_input(
                "Nama Produk *",
                placeholder="Contoh: Laptop ASUS ROG 15",
            )

            # Pilihan Kategori (Relasi Aggregation)
            opsi_kat = {"-- Tanpa Kategori --": None}
            for k in daftar_kategori:
                opsi_kat[f"📁 {k.nama}"] = k.id

            kat_terpilih = st.selectbox(
                "Kategori Produk",
                options=list(opsi_kat.keys()),
            )
            kategori_id = opsi_kat[kat_terpilih]

            col_harga, col_stok = st.columns(2)
            with col_harga:
                harga_produk = st.number_input(
                    "Harga Satuan (Rp) *",
                    min_value=0.0,
                    step=1000.0,
                    format="%.2f",
                )
            with col_stok:
                stok_produk = st.number_input(
                    "Jumlah Stok *",
                    min_value=0,
                    step=1,
                    value=0,
                )

            st.write("")
            col_sub, _ = st.columns([1, 4])
            with col_sub:
                submitted = st.form_submit_button("💾 Simpan Produk", type="primary")

            if submitted:
                try:
                    controller.tambah_produk(
                        nama=nama_produk,
                        harga=harga_produk,
                        stok=stok_produk,
                        kategori_id=kategori_id,
                    )
                    st.session_state["flash_message"] = {
                        "type": "success",
                        "text": f"Produk '{nama_produk}' berhasil ditambahkan!",
                    }
                    st.session_state["produk_mode"] = "daftar"
                    st.rerun()
                except ValueError as err:
                    st.error(f"❌ {str(err)}")
                except Exception as err:
                    st.error(f"❌ Terjadi kesalahan: {str(err)}")

    # ==============================================================
    # 2. HALAMAN EDIT PRODUK
    # ==============================================================
    elif mode == "edit":
        if st.button("⬅️ Kembali ke Daftar Produk"):
            st.session_state["produk_mode"] = "daftar"
            st.session_state["produk_edit_id"] = None
            st.rerun()

        edit_id = st.session_state.get("produk_edit_id")
        produk = controller.ambil_produk(edit_id) if edit_id else None

        if not produk:
            st.error("Data produk tidak ditemukan atau mungkin sudah dihapus.")
            if st.button("Kembali ke Daftar"):
                st.session_state["produk_mode"] = "daftar"
                st.rerun()
            return

        st.title(f"✏️ Edit Data Produk: {produk.nama}")
        st.info(f"ℹ️ **Informasi Produk (`get_info()`):** {produk.get_info()}")

        with st.form("form_edit_produk", clear_on_submit=False):
            nama_edit = st.text_input("Nama Produk *", value=produk.nama)

            # Pilihan Kategori
            opsi_kat = {"-- Tanpa Kategori --": None}
            idx_pilih = 0
            for i, k in enumerate(daftar_kategori, start=1):
                opsi_kat[f"📁 {k.nama}"] = k.id
                if produk.kategori_id == k.id:
                    idx_pilih = i

            kat_terpilih = st.selectbox(
                "Kategori Produk",
                options=list(opsi_kat.keys()),
                index=idx_pilih,
            )
            kategori_id_edit = opsi_kat[kat_terpilih]

            col_h, col_s = st.columns(2)
            with col_h:
                harga_edit = st.number_input(
                    "Harga Satuan (Rp) *",
                    min_value=0.0,
                    step=1000.0,
                    value=float(produk.harga),
                    format="%.2f",
                )
            with col_s:
                stok_edit = st.number_input(
                    "Jumlah Stok *",
                    min_value=0,
                    step=1,
                    value=int(produk.stok),
                )

            st.write("")
            col_sub, _ = st.columns([1, 4])
            with col_sub:
                submitted_edit = st.form_submit_button("💾 Simpan Perubahan", type="primary")

            if submitted_edit:
                try:
                    controller.ubah_produk(
                        produk_id=produk.id,
                        nama=nama_edit,
                        harga=harga_edit,
                        stok=stok_edit,
                        kategori_id=kategori_id_edit,
                    )
                    st.session_state["flash_message"] = {
                        "type": "success",
                        "text": f"Data produk '{nama_edit}' berhasil diperbarui!",
                    }
                    st.session_state["produk_mode"] = "daftar"
                    st.session_state["produk_edit_id"] = None
                    st.rerun()
                except ValueError as err:
                    st.error(f"❌ {str(err)}")
                except Exception as err:
                    st.error(f"❌ Terjadi kesalahan: {str(err)}")

    # ==============================================================
    # 3. HALAMAN UTAMA: DAFTAR PRODUK (DEFAULT)
    # ==============================================================
    else:
        st.title("🛍️ Manajemen Produk")
        st.caption(
            "Mengimplementasikan entitas **Produk** dengan method `get_info()` "
            "dan relasi Aggregation dengan **Kategori** (`Kategori.daftar_produk`)."
        )

        semua_produk = controller.semua_produk()

        # Statistik Ringkasan di atas
        if semua_produk:
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Jenis Produk", f"{len(semua_produk)} jenis")
            m2.metric("Total Seluruh Stok", f"{sum(p.stok for p in semua_produk):,} unit")
            m3.metric(
                "Estimasi Total Nilai",
                f"Rp {sum(p.harga * p.stok for p in semua_produk):,.2f}",
            )
            st.write("")

        # Bagian Atas Tabel: Pencarian & Tombol Tambah Data
        col_cari, col_kat_filter, col_tambah = st.columns([2.5, 1.5, 1.2], vertical_alignment="bottom")
        with col_cari:
            cari = st.text_input(
                "🔍 Cari Produk:",
                placeholder="Ketik nama produk...",
                key="cari_produk_input",
            )
        with col_kat_filter:
            opsi_filter = ["Semua Kategori"] + [k.nama for k in daftar_kategori]
            filter_kat = st.selectbox("Filter Kategori:", options=opsi_filter)
        with col_tambah:
            if st.button("➕ Tambah Data", type="primary", use_container_width=True):
                st.session_state["produk_mode"] = "tambah"
                st.rerun()

        # Filter produk
        produk_tampil = semua_produk
        if cari:
            produk_tampil = [p for p in produk_tampil if cari.lower() in p.nama.lower()]
        if filter_kat != "Semua Kategori":
            produk_tampil = [
                p for p in produk_tampil if p.kategori and p.kategori.nama == filter_kat
            ]

        st.write("")

        # Tampilkan Tabel Produk
        if not semua_produk:
            st.info(
                "📦 Belum ada data produk di database. Klik tombol **'➕ Tambah Data'** di atas untuk menambahkan produk pertama."
            )
        elif not produk_tampil:
            st.warning("Tidak ada produk yang cocok dengan filter pencarian.")
        else:
            # Header Tabel
            st.markdown("---")
            col_id, col_nm, col_kt, col_hg, col_st, col_tot, col_act = st.columns(
                [0.7, 2.5, 1.8, 1.6, 1.0, 1.6, 1.8], vertical_alignment="center"
            )
            col_id.markdown("**ID**")
            col_nm.markdown("**Nama Produk**")
            col_kt.markdown("**Kategori**")
            col_hg.markdown("**Harga**")
            col_st.markdown("**Stok**")
            col_tot.markdown("**Total Nilai**")
            col_act.markdown("<div style='text-align: center;'><b>Aksi</b></div>", unsafe_allow_html=True)
            st.markdown("---")

            # Baris Data Produk
            for p in produk_tampil:
                c_id, c_nm, c_kt, c_hg, c_st, c_tot, c_act = st.columns(
                    [0.7, 2.5, 1.8, 1.6, 1.0, 1.6, 1.8], vertical_alignment="center"
                )
                c_id.write(f"#{p.id}")
                c_nm.markdown(f"**{p.nama}**")
                c_kt.write(p.kategori.nama if p.kategori else "-")
                c_hg.write(f"Rp {p.harga:,.2f}")
                c_st.write(f"{p.stok:,}")
                c_tot.write(f"Rp {p.harga * p.stok:,.2f}")

                with c_act:
                    b_edit, b_del = st.columns(2)
                    with b_edit:
                        if st.button("✏️ Edit", key=f"btn_edit_{p.id}", use_container_width=True):
                            st.session_state["produk_mode"] = "edit"
                            st.session_state["produk_edit_id"] = p.id
                            st.rerun()
                    with b_del:
                        if st.button("🗑️ Hapus", key=f"btn_del_{p.id}", type="secondary", use_container_width=True):
                            konfirmasi_hapus_dialog(p.id, p.nama, controller)

                st.markdown(
                    "<hr style='margin: 0.25rem 0; border: none; border-top: 1px solid #f1f3f5;'>",
                    unsafe_allow_html=True,
                )
