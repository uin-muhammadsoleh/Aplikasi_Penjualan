import streamlit as st


def _val_stok(p) -> int:
    """Mengambil stok produk dengan aman (mendukung atribut stok maupun method get_stok)."""
    if hasattr(p, "get_stok") and callable(getattr(p, "get_stok")):
        try:
            return int(p.get_stok())
        except Exception:
            pass
    return int(getattr(p, "stok", 0) or 0)


def _val_harga(p) -> float:
    """Mengambil harga produk dengan aman (mendukung atribut harga maupun method get_harga)."""
    if hasattr(p, "get_harga") and callable(getattr(p, "get_harga")):
        try:
            return float(p.get_harga())
        except Exception:
            pass
    return float(getattr(p, "harga", 0.0) or 0.0)


def _val_nama(obj) -> str:
    """Mengambil nama entitas dengan aman (mendukung atribut nama maupun method get_nama)."""
    if hasattr(obj, "get_nama") and callable(getattr(obj, "get_nama")):
        try:
            return str(obj.get_nama())
        except Exception:
            pass
    return str(getattr(obj, "nama", "") or "")


def _val_kat_id(p) -> int | None:
    """Mengambil ID kategori produk dengan aman."""
    if hasattr(p, "get_kategori_id") and callable(getattr(p, "get_kategori_id")):
        try:
            return p.get_kategori_id()
        except Exception:
            pass
    return getattr(p, "kategori_id", None)


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
    """Menampilkan antarmuka manajemen produk dengan validasi input,
    peringatan di bawah masing-masing textbox, serta integrasi getter/setter yang aman.
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
        st.caption("Tambahkan produk baru dengan validasi data dan relasi Kategori (Aggregation).")

        with st.form("form_tambah_produk", clear_on_submit=False):
            nama_produk = st.text_input(
                "Nama Produk *",
                placeholder="Contoh: Laptop ASUS ROG 15",
            )
            # Peringatan error tepat di bawah textbox Nama Produk
            err_nama = st.empty()

            # Pilihan Kategori (Relasi Aggregation)
            opsi_kat = {"-- Tanpa Kategori --": None}
            for k in daftar_kategori:
                opsi_kat[f"📁 {_val_nama(k)}"] = k.id

            kat_terpilih = st.selectbox(
                "Kategori Produk",
                options=list(opsi_kat.keys()),
            )
            kategori_id = opsi_kat[kat_terpilih]
            err_kategori = st.empty()

            col_harga, col_stok = st.columns(2)
            with col_harga:
                harga_produk = st.number_input(
                    "Harga Satuan (Rp) *",
                    min_value=0.0,
                    step=1000.0,
                    format="%.2f",
                )
                # Peringatan error tepat di bawah textbox/input Harga
                err_harga = st.empty()

            with col_stok:
                stok_produk = st.number_input(
                    "Jumlah Stok *",
                    min_value=0,
                    step=1,
                    value=0,
                )
                # Peringatan error tepat di bawah textbox/input Stok
                err_stok = st.empty()

            st.write("")
            col_sub, _ = st.columns([1, 4])
            with col_sub:
                submitted = st.form_submit_button("💾 Simpan Produk", type="primary")

            if submitted:
                ada_error = False

                # 1. Validasi Nama Produk
                if not nama_produk or len(nama_produk.strip()) < 2:
                    err_nama.error("⚠️ Data input salah: Nama produk wajib diisi (minimal 2 karakter).")
                    ada_error = True
                elif len(nama_produk.strip()) > 150:
                    err_nama.error("⚠️ Data input salah: Nama produk maksimal 150 karakter.")
                    ada_error = True

                # 2. Validasi Harga Produk
                if harga_produk is None or harga_produk < 0:
                    err_harga.error("⚠️ Data input salah: Harga tidak boleh bernilai negatif (minimal Rp 0).")
                    ada_error = True

                # 3. Validasi Stok Produk
                if stok_produk is None or stok_produk < 0:
                    err_stok.error("⚠️ Data input salah: Jumlah stok tidak boleh negatif (minimal 0).")
                    ada_error = True

                # Jika seluruh validasi lolos, teruskan ke Controller
                if not ada_error:
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
                        err_nama.error(f"⚠️ Data input tidak sesuai: {str(err)}")
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

        nama_prod_ini = _val_nama(produk)
        st.title(f"✏️ Edit Data Produk: {nama_prod_ini}")
        if hasattr(produk, "get_info") and callable(getattr(produk, "get_info")):
            st.info(f"ℹ️ **Informasi Produk (`get_info()`):** {produk.get_info()}")

        with st.form("form_edit_produk", clear_on_submit=False):
            nama_edit = st.text_input("Nama Produk *", value=nama_prod_ini)
            # Peringatan error tepat di bawah textbox Nama Produk
            err_nama_edit = st.empty()

            # Pilihan Kategori
            opsi_kat = {"-- Tanpa Kategori --": None}
            idx_pilih = 0
            cur_kat_id = _val_kat_id(produk)
            for i, k in enumerate(daftar_kategori, start=1):
                opsi_kat[f"📁 {_val_nama(k)}"] = k.id
                if cur_kat_id == k.id:
                    idx_pilih = i

            kat_terpilih = st.selectbox(
                "Kategori Produk",
                options=list(opsi_kat.keys()),
                index=idx_pilih,
            )
            kategori_id_edit = opsi_kat[kat_terpilih]
            err_kategori_edit = st.empty()

            col_h, col_s = st.columns(2)
            with col_h:
                harga_edit = st.number_input(
                    "Harga Satuan (Rp) *",
                    min_value=0.0,
                    step=1000.0,
                    value=float(_val_harga(produk)),
                    format="%.2f",
                )
                # Peringatan error tepat di bawah textbox/input Harga
                err_harga_edit = st.empty()

            with col_s:
                stok_edit = st.number_input(
                    "Jumlah Stok *",
                    min_value=0,
                    step=1,
                    value=int(_val_stok(produk)),
                )
                # Peringatan error tepat di bawah textbox/input Stok
                err_stok_edit = st.empty()

            st.write("")
            col_sub, _ = st.columns([1, 4])
            with col_sub:
                submitted_edit = st.form_submit_button("💾 Simpan Perubahan", type="primary")

            if submitted_edit:
                ada_error = False

                # 1. Validasi Nama Produk
                if not nama_edit or len(nama_edit.strip()) < 2:
                    err_nama_edit.error("⚠️ Data input salah: Nama produk wajib diisi (minimal 2 karakter).")
                    ada_error = True
                elif len(nama_edit.strip()) > 150:
                    err_nama_edit.error("⚠️ Data input salah: Nama produk maksimal 150 karakter.")
                    ada_error = True

                # 2. Validasi Harga Produk
                if harga_edit is None or harga_edit < 0:
                    err_harga_edit.error("⚠️ Data input salah: Harga tidak boleh bernilai negatif (minimal Rp 0).")
                    ada_error = True

                # 3. Validasi Stok Produk
                if stok_edit is None or stok_edit < 0:
                    err_stok_edit.error("⚠️ Data input salah: Jumlah stok tidak boleh negatif (minimal 0).")
                    ada_error = True

                if not ada_error:
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
                        err_nama_edit.error(f"⚠️ Data input tidak sesuai: {str(err)}")
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
            m2.metric("Total Seluruh Stok", f"{sum(_val_stok(p) for p in semua_produk):,} unit")
            m3.metric(
                "Estimasi Total Nilai",
                f"Rp {sum(_val_harga(p) * _val_stok(p) for p in semua_produk):,.2f}",
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
            opsi_filter = ["Semua Kategori"] + [_val_nama(k) for k in daftar_kategori]
            filter_kat = st.selectbox("Filter Kategori:", options=opsi_filter)
        with col_tambah:
            if st.button("➕ Tambah Data", type="primary", use_container_width=True):
                st.session_state["produk_mode"] = "tambah"
                st.rerun()

        # Filter produk
        produk_tampil = semua_produk
        if cari:
            produk_tampil = [p for p in produk_tampil if cari.lower() in _val_nama(p).lower()]
        if filter_kat != "Semua Kategori":
            produk_tampil = [
                p for p in produk_tampil if p.kategori and _val_nama(p.kategori) == filter_kat
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
                c_nm.markdown(f"**{_val_nama(p)}**")
                c_kt.write(_val_nama(p.kategori) if p.kategori else "-")
                c_hg.write(f"Rp {_val_harga(p):,.2f}")
                c_st.write(f"{_val_stok(p):,}")
                c_tot.write(f"Rp {_val_harga(p) * _val_stok(p):,.2f}")

                with c_act:
                    b_edit, b_del = st.columns(2)
                    with b_edit:
                        if st.button("✏️ Edit", key=f"btn_edit_{p.id}", use_container_width=True):
                            st.session_state["produk_mode"] = "edit"
                            st.session_state["produk_edit_id"] = p.id
                            st.rerun()
                    with b_del:
                        if st.button("🗑️ Hapus", key=f"btn_del_{p.id}", type="secondary", use_container_width=True):
                            konfirmasi_hapus_dialog(p.id, _val_nama(p), controller)

                st.markdown(
                    "<hr style='margin: 0.25rem 0; border: none; border-top: 1px solid #f1f3f5;'>",
                    unsafe_allow_html=True,
                )
