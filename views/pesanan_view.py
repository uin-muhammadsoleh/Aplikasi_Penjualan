import pandas as pd
import streamlit as st
from controllers.pelanggan_controller import PelangganController
from controllers.pesanan_controller import PesananController
from controllers.produk_controller import ProdukController


def tampilkan_halaman_pesanan(
    pesanan_ctrl: PesananController,
    produk_ctrl: ProdukController,
    pelanggan_ctrl: PelangganController,
):
    st.title("🏷️ Manajemen Pesanan & Transaksi")
    st.caption(
        "Mengimplementasikan entitas **Pesanan** (`nomor`, `detail`, `+ tambah_produk()`) "
        "dan **DetailPesanan** (`produk`, `jumlah`, `+ get_total()`) dengan relasi **Composition**."
    )

    tab_daftar, tab_buat = st.tabs(["📋 Riwayat Pesanan", "➕ Buat Pesanan Baru"])

    semua_pesanan = pesanan_ctrl.semua_pesanan()

    with tab_daftar:
        st.subheader("Daftar Transaksi Pesanan")
        if semua_pesanan:
            for pes in semua_pesanan:
                pel_nama = pes.pelanggan.get_nama() if pes.pelanggan else "Umum"
                with st.expander(
                    f"📦 No. Pesanan: **{pes.get_nomor()}** | Pelanggan: **{pel_nama}** | Total: **Rp {pes.get_total_pesanan():,.2f}**"
                ):
                    st.caption(f"Waktu Transaksi: {pes.get_tanggal().strftime('%Y-%m-%d %H:%M:%S')}")
                    st.write("#### Rincian Item (Composition: `DetailPesanan`):")

                    data_detail = []
                    for idx, d in enumerate(pes.get_detail(), start=1):
                        prod = d.get_produk()
                        data_detail.append(
                            {
                                "No": idx,
                                "Nama Produk": prod.get_nama() if prod else "-",
                                "Harga Satuan": f"Rp {prod.get_harga():,.2f}" if prod else "-",
                                "Jumlah (Qty)": d.get_jumlah(),
                                "Subtotal (`get_total()`)": f"Rp {d.get_total():,.2f}",
                            }
                        )

                    st.dataframe(pd.DataFrame(data_detail), use_container_width=True, hide_index=True)
                    st.markdown(
                        f"### Total Keseluruhan: <span style='color: green;'>Rp {pes.get_total_pesanan():,.2f}</span>",
                        unsafe_allow_html=True,
                    )
        else:
            st.info("Belum ada transaksi pesanan.")

    with tab_buat:
        st.subheader("Formulir Pemesanan Baru")
        semua_produk = produk_ctrl.semua_produk()
        semua_pelanggan = pelanggan_ctrl.semua_pelanggan()

        if not semua_produk:
            st.warning("Belum ada produk yang dapat dipesan. Silakan tambahkan produk terlebih dahulu.")
            return

        nomor_pesanan_auto = pesanan_ctrl.generate_nomor_pesanan()

        nomor_pesanan = st.text_input("Nomor Pesanan *", value=nomor_pesanan_auto)
        # Peringatan error tepat di bawah textbox Nomor Pesanan
        err_nomor = st.empty()

        opsi_pel = {f"#{p.id} - {p.get_nama()}": p.id for p in semua_pelanggan}
        pel_terpilih = st.selectbox(
            "Pilih Pelanggan *",
            options=list(opsi_pel.keys()) if opsi_pel else ["(Tidak ada pelanggan)"],
        )
        pelanggan_id = opsi_pel.get(pel_terpilih) if opsi_pel else None
        # Peringatan error tepat di bawah selectbox Pelanggan
        err_pelanggan = st.empty()

        st.write("---")
        st.markdown("#### Pilih Produk & Jumlah Pembelian")

        if "cart_items" not in st.session_state:
            st.session_state["cart_items"] = []

        opsi_prod = {
            f"{p.get_nama()} (Stok: {p.get_stok()}, Rp {p.get_harga():,.0f})": p
            for p in semua_produk
            if p.get_stok() > 0
        }

        if opsi_prod:
            col_p, col_q, col_btn = st.columns([3, 1, 1], vertical_alignment="bottom")
            with col_p:
                prod_label = st.selectbox("Pilih Produk:", options=list(opsi_prod.keys()))
                prod_obj = opsi_prod[prod_label]
            with col_q:
                qty = st.number_input(
                    "Jumlah *",
                    min_value=1,
                    value=1,
                    step=1,
                )
            with col_btn:
                btn_tambah_item = st.button("➕ Tambah ke Item")

            # Peringatan error tepat di bawah input Jumlah / Pilihan Produk
            err_qty = st.empty()

            if btn_tambah_item:
                if qty <= 0:
                    err_qty.error("⚠️ Data input salah: Jumlah pembelian minimal 1 item.")
                elif qty > prod_obj.get_stok():
                    err_qty.error(
                        f"⚠️ Data input salah: Jumlah ({qty}) melebihi stok yang tersedia ({prod_obj.get_stok()} unit)."
                    )
                else:
                    # Cek apakah item sudah ada di cart
                    ada_di_cart = False
                    for item in st.session_state["cart_items"]:
                        if item["produk_id"] == prod_obj.id:
                            total_qty = item["jumlah"] + qty
                            if total_qty > prod_obj.get_stok():
                                err_qty.error(
                                    f"⚠️ Data input salah: Total jumlah di keranjang ({total_qty}) melebihi stok ({prod_obj.get_stok()})."
                                )
                                ada_di_cart = True
                                break
                            item["jumlah"] = total_qty
                            item["subtotal"] = prod_obj.get_harga() * total_qty
                            ada_di_cart = True
                            st.rerun()

                    if not ada_di_cart:
                        st.session_state["cart_items"].append(
                            {
                                "produk_id": prod_obj.id,
                                "nama": prod_obj.get_nama(),
                                "harga": prod_obj.get_harga(),
                                "jumlah": qty,
                                "subtotal": prod_obj.get_harga() * qty,
                            }
                        )
                        st.rerun()

            if st.session_state["cart_items"]:
                st.write("##### Daftar Produk dalam Pesanan:")
                st.dataframe(
                    pd.DataFrame(st.session_state["cart_items"]),
                    use_container_width=True,
                    hide_index=True,
                )
                total_belanja = sum(i["subtotal"] for i in st.session_state["cart_items"])
                st.markdown(f"#### Total Estimasi: **Rp {total_belanja:,.2f}**")

                err_cart = st.empty()

                col_sv, col_rst = st.columns([1, 4])
                with col_sv:
                    if st.button("💾 Proses & Simpan Pesanan", type="primary"):
                        ada_err_order = False

                        # Validasi nomor pesanan
                        nomor_clean = (nomor_pesanan or "").strip()
                        if not nomor_clean or len(nomor_clean) < 3:
                            err_nomor.error("⚠️ Data input salah: Nomor pesanan wajib diisi (minimal 3 karakter).")
                            ada_err_order = True

                        # Validasi pelanggan
                        if not pelanggan_id:
                            err_pelanggan.error("⚠️ Data input salah: Silakan pilih pelanggan yang terdaftar.")
                            ada_err_order = True

                        # Validasi item
                        if not st.session_state["cart_items"]:
                            err_cart.error("⚠️ Data input salah: Pesanan minimal harus memiliki 1 item produk.")
                            ada_err_order = True

                        if not ada_err_order:
                            try:
                                items_payload = [
                                    {"produk_id": i["produk_id"], "jumlah": i["jumlah"]}
                                    for i in st.session_state["cart_items"]
                                ]
                                pesanan_ctrl.buat_pesanan(
                                    nomor=nomor_clean,
                                    pelanggan_id=pelanggan_id,
                                    list_item=items_payload,
                                )
                                st.session_state["cart_items"] = []
                                st.success(f"Pesanan '{nomor_clean}' berhasil dibuat!")
                                st.rerun()
                            except ValueError as err:
                                err_cart.error(f"⚠️ Data input tidak sesuai: {err}")
                            except Exception as err:
                                err_cart.error(f"Gagal memproses pesanan: {err}")
                with col_rst:
                    if st.button("Kosongkan Keranjang"):
                        st.session_state["cart_items"] = []
                        st.rerun()
        else:
            st.warning("Semua produk saat ini sedang habis stoknya.")
