import streamlit as st
from controllers.auth_controller import AuthController


def tampilkan_halaman_auth(controller: AuthController):
    """Menampilkan antarmuka login dan registrasi pengguna."""
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
                    "Username",
                    placeholder="Masukkan username Anda...",
                    key="login_username",
                )
                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Masukkan password Anda...",
                    key="login_password",
                )
                submitted = st.form_submit_button(
                    "🚀 Masuk ke Aplikasi",
                    type="primary",
                    use_container_width=True,
                )

                if submitted:
                    success, message, user = controller.login_user(username, password)
                    if success and user:
                        controller.login_session(user)
                        st.success(f"Selamat datang, {user.nama_lengkap}! Mengalihkan...")
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")

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
                    "Nama Lengkap",
                    placeholder="Contoh: Budi Santoso",
                    key="reg_nama",
                )
                reg_username = st.text_input(
                    "Username",
                    placeholder="Contoh: budi_s",
                    help="Minimal 3 karakter, hanya huruf, angka, dan underscore (_).",
                    key="reg_username",
                )
                reg_password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Minimal 6 karakter...",
                    key="reg_password",
                )
                reg_konfirmasi = st.text_input(
                    "Konfirmasi Password",
                    type="password",
                    placeholder="Ulangi password di atas...",
                    key="reg_konfirmasi",
                )
                submit_reg = st.form_submit_button(
                    "✨ Daftarkan Akun",
                    type="primary",
                    use_container_width=True,
                )

                if submit_reg:
                    success, message = controller.daftar_user(
                        reg_username, reg_password, reg_konfirmasi, nama_lengkap
                    )
                    if success:
                        st.success(f"✅ {message}")
                        st.info("Silakan beralih ke tab **Masuk (Login)** untuk mulai menggunakan akun.")
                    else:
                        st.error(f"❌ {message}")
