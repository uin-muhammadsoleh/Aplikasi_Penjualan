import re
import streamlit as st
from controllers.auth_controller import AuthController


def tampilkan_halaman_auth(controller: AuthController):
    """Menampilkan antarmuka login dan registrasi pengguna dengan validasi data
    dan pesan peringatan langsung di bawah setiap textbox input.
    """
    st.markdown(
        """
        <style>
            .auth-container {
                max-width: 480px;
                margin: 0 auto;
                padding: 1.5rem;
            }
            .auth-header {
                text-align: center;
                margin-bottom: 1.5rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    _, col, _ = st.columns([1, 2, 1])

    with col:
        st.markdown(
            """
            <div class="auth-header">
                <h2>🔐 Sistem Masuk</h2>
                <p style="color: #6c757d;">Silakan masuk ke akun Anda atau daftar untuk mengakses aplikasi Manajemen Produk.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        tab_login, tab_register = st.tabs(["🔑 Masuk (Login)", "📝 Buat Akun (Register)"])

        with tab_login:
            st.write("")
            with st.form("form_login", clear_on_submit=False):
                username = st.text_input(
                    "Username *",
                    placeholder="Masukkan username Anda...",
                    key="login_username",
                )
                # Peringatan error tepat di bawah textbox username
                err_login_user = st.empty()

                password = st.text_input(
                    "Password *",
                    type="password",
                    placeholder="Masukkan password Anda...",
                    key="login_password",
                )
                # Peringatan error tepat di bawah textbox password
                err_login_pass = st.empty()

                submitted = st.form_submit_button(
                    "🚀 Masuk ke Aplikasi",
                    type="primary",
                    use_container_width=True,
                )

                if submitted:
                    ada_error_login = False
                    user_clean = (username or "").strip()
                    pass_clean = password or ""

                    if not user_clean:
                        err_login_user.error("⚠️ Data input salah: Username wajib diisi.")
                        ada_error_login = True

                    if not pass_clean:
                        err_login_pass.error("⚠️ Data input salah: Password wajib diisi.")
                        ada_error_login = True

                    if not ada_error_login:
                        success, message, user = controller.login_user(user_clean, pass_clean)
                        if success and user:
                            controller.login_session(user)
                            st.success(f"Selamat datang, {user.get_nama_lengkap()}! Mengalihkan...")
                            st.rerun()
                        else:
                            err_login_pass.error(f"⚠️ Data input salah: {message}")

            st.markdown("---")
            st.info(
                "💡 **Akun Bawaan (Default):**\n\n"
                "- **Username:** `admin`\n"
                "- **Password:** `admin123`"
            )

        with tab_register:
            st.write("")
            with st.form("form_register", clear_on_submit=False):
                nama_lengkap = st.text_input(
                    "Nama Lengkap *",
                    placeholder="Contoh: Budi Santoso",
                    key="reg_nama",
                )
                # Peringatan error tepat di bawah textbox Nama Lengkap
                err_reg_nama = st.empty()

                reg_username = st.text_input(
                    "Username *",
                    placeholder="Contoh: budi_s",
                    help="Minimal 3 karakter, hanya huruf, angka, dan underscore (_).",
                    key="reg_username",
                )
                # Peringatan error tepat di bawah textbox Username
                err_reg_user = st.empty()

                reg_password = st.text_input(
                    "Password *",
                    type="password",
                    placeholder="Minimal 6 karakter...",
                    key="reg_password",
                )
                # Peringatan error tepat di bawah textbox Password
                err_reg_pass = st.empty()

                reg_konfirmasi = st.text_input(
                    "Konfirmasi Password *",
                    type="password",
                    placeholder="Ulangi password di atas...",
                    key="reg_konfirmasi",
                )
                # Peringatan error tepat di bawah textbox Konfirmasi Password
                err_reg_konf = st.empty()

                submit_reg = st.form_submit_button(
                    "✨ Daftarkan Akun",
                    type="primary",
                    use_container_width=True,
                )

                if submit_reg:
                    ada_error_reg = False
                    nama_clean = (nama_lengkap or "").strip()
                    user_clean = (reg_username or "").strip().lower()
                    pwd_clean = reg_password or ""
                    konf_clean = reg_konfirmasi or ""

                    # 1. Validasi Nama Lengkap
                    if not nama_clean or len(nama_clean) < 2:
                        err_reg_nama.error("⚠️ Data input salah: Nama lengkap wajib diisi (minimal 2 karakter).")
                        ada_error_reg = True
                    elif len(nama_clean) > 100:
                        err_reg_nama.error("⚠️ Data input salah: Nama lengkap maksimal 100 karakter.")
                        ada_error_reg = True

                    # 2. Validasi Username
                    if not user_clean:
                        err_reg_user.error("⚠️ Data input salah: Username wajib diisi.")
                        ada_error_reg = True
                    elif len(user_clean) < 3 or len(user_clean) > 30:
                        err_reg_user.error("⚠️ Data input salah: Username harus 3 hingga 30 karakter.")
                        ada_error_reg = True
                    elif not re.match(r"^[a-zA-Z0-9_]+$", user_clean):
                        err_reg_user.error("⚠️ Data input salah: Username hanya boleh huruf, angka, dan underscore (_).")
                        ada_error_reg = True

                    # 3. Validasi Password
                    if not pwd_clean:
                        err_reg_pass.error("⚠️ Data input salah: Password wajib diisi.")
                        ada_error_reg = True
                    elif len(pwd_clean) < 6:
                        err_reg_pass.error("⚠️ Data input salah: Password minimal 6 karakter.")
                        ada_error_reg = True

                    # 4. Validasi Konfirmasi Password
                    if not konf_clean:
                        err_reg_konf.error("⚠️ Data input salah: Konfirmasi password wajib diisi.")
                        ada_error_reg = True
                    elif pwd_clean != konf_clean:
                        err_reg_konf.error("⚠️ Data input salah: Konfirmasi password tidak cocok dengan password di atas.")
                        ada_error_reg = True

                    if not ada_error_reg:
                        success, message = controller.daftar_user(
                            user_clean, pwd_clean, konf_clean, nama_clean
                        )
                        if success:
                            st.success(f"✅ {message}")
                            st.info("Silakan beralih ke tab **Masuk (Login)** untuk mulai menggunakan akun.")
                        else:
                            if "Username" in message and "sudah terdaftar" in message:
                                err_reg_user.error(f"⚠️ Data input salah: {message}")
                            else:
                                st.error(f"❌ {message}")
