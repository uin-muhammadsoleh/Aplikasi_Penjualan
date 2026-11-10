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
                with st.expander(
                    f"📦 No. Pesanan: **{pes.nomor}** | Pelanggan: **{pes.pelanggan.nama if pes.pelanggan else 'Umum'}** | Total: **Rp {pes.get_total_pesanan():,.2f}**"
                ):
                    st.caption(f"Waktu Transaksi: {pes.tanggal.strftime('%Y-%m-%d %H:%M:%S')}")
                    st.write("#### Rincian Item (Composition: `DetailPesanan`):")

                    data_detail = []
                    for idx, d in enumerate(pes.detail, start=1):
                        data_detail.append(
                            {
                                "No": idx,
                                "Nama Produk": d.produk.nama if d.produk else "-",
                                "Harga Satuan": f"Rp {d.produk.harga:,.2f}" if d.produk else "-",
                                "Jumlah (Qty)": d.jumlah,
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

        nomor_pesanan = st.text_input("Nomor Pesanan", value=nomor_pesanan_auto)

        opsi_pel = {f"#{p.id} - {p.nama}": p.id for p in semua_pelanggan}
        pel_terpilih = st.selectbox(
            "Pilih Pelanggan:",
            options=list(opsi_pel.keys()) if opsi_pel else ["(Tidak ada pelanggan)"],
        )
        pelanggan_id = opsi_pel.get(pel_terpilih) if opsi_pel else None

        st.write("---")
        st.markdown("#### Pilih Produk & Jumlah Pembelian")

        if "cart_items" not in st.session_state:
            st.session_state["cart_items"] = []

        opsi_prod = {
            f"{p.nama} (Stok: {p.stok}, Rp {p.harga:,.0f})": p for p in semua_produk if p.stok > 0
        }

        if opsi_prod:
            col_p, col_q, col_btn = st.columns([3, 1, 1], vertical_alignment="bottom")
            with col_p:
                prod_label = st.selectbox("Pilih Produk:", options=list(opsi_prod.keys()))
                prod_obj = opsi_prod[prod_label]
            with col_q:
                qty = st.number_input(
                    "Jumlah",
                    min_value=1,
                    max_value=max(1, prod_obj.stok),
                    value=1,
                    step=1,
                )
            with col_btn:
                if st.button("➕ Tambah ke Item"):
                    st.session_state["cart_items"].append(
                        {
                            "produk_id": prod_obj.id,
                            "nama": prod_obj.nama,
                            "harga": prod_obj.harga,
                            "jumlah": qty,
                            "subtotal": prod_obj.harga * qty,
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

                col_sv, col_rst = st.columns([1, 4])
                with col_sv:
                    if st.button("💾 Proses & Simpan Pesanan", type="primary"):
                        try:
                            items_payload = [
                                {"produk_id": i["produk_id"], "jumlah": i["jumlah"]}
                                for i in st.session_state["cart_items"]
                            ]
                            pesanan_ctrl.buat_pesanan(
                                nomor=nomor_pesanan,
                                pelanggan_id=pelanggan_id,
                                list_item=items_payload,
                            )
                            st.session_state["cart_items"] = []
                            st.success(f"Pesanan '{nomor_pesanan}' berhasil dibuat!")
                            st.rerun()
                        except Exception as err:
                            st.error(f"Gagal memproses pesanan: {err}")
                with col_rst:
                    if st.button("Kosongkan Keranjang"):
                        st.session_state["cart_items"] = []
                        st.rerun()
        else:
            st.warning("Semua produk saat ini sedang habis stoknya.")
