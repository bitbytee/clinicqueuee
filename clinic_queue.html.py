import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date, timedelta
import random

# ==========================================================
# CLINIC QUEUE SYSTEM
# Python dasar + Tkinter (tanpa library tambahan)
# Jalankan: python clinic_queue.py
# ==========================================================

APP_NAME = "Clinic Queue"
BG = "#F4F7FB"
CARD = "#FFFFFF"
NAVY = "#182544"
MUTED = "#7B879D"
BLUE = "#4263EB"
BLUE_DARK = "#304ACB"
TEAL = "#14B8A6"
GREEN = "#16A879"
RED = "#E65365"
BORDER = "#E6EBF2"
FONT = "Segoe UI"


class ClinicQueueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clinic Queue | Sistem Antrean Klinik")
        self.root.geometry("1180x760")
        self.root.minsize(980, 650)
        self.root.configure(bg=BG)

        self.user_nim = ""
        self.user_name = ""
        self.current_page = "Beranda"
        self.bookings = []
        self.selected_booking = None

        self.faskes_data = {
            "Klinik Sehat Sentosa": {
                "dokter": ["dr. Alya Putri", "dr. Bima Pratama", "dr. Citra Ananda"],
                "poli": ["Poli Umum", "Poli Gigi", "Poli Anak"]
            },
            "Puskesmas Harmoni": {
                "dokter": ["dr. Dimas Saputra", "dr. Nabila Rahma", "dr. Raka Wijaya"],
                "poli": ["Poli Umum", "Poli Gigi", "Poli Ibu dan Anak"]
            },
            "Klinik Medika Plus": {
                "dokter": ["dr. Farah Lestari", "dr. Gilang Mahesa", "dr. Hana Safitri"],
                "poli": ["Poli Umum", "Poli Gigi", "Poli Kulit"]
            }
        }

        self._setup_styles()
        self.show_login()

    def _setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure(
            "Modern.TCombobox",
            fieldbackground="#FFFFFF",
            background="#FFFFFF",
            foreground=NAVY,
            padding=9,
            arrowsize=14
        )
        style.map(
            "Modern.TCombobox",
            fieldbackground=[("readonly", "#FFFFFF")],
            foreground=[("readonly", NAVY)]
        )
        style.configure(
            "Modern.Treeview",
            background="#FFFFFF",
            fieldbackground="#FFFFFF",
            foreground=NAVY,
            rowheight=36,
            borderwidth=0,
            font=(FONT, 10)
        )
        style.configure(
            "Modern.Treeview.Heading",
            background="#F0F4FA",
            foreground="#58657C",
            relief="flat",
            font=(FONT, 9, "bold"),
            padding=9
        )
        style.map("Modern.Treeview", background=[("selected", "#E7EDFF")],
                  foreground=[("selected", NAVY)])

    # ---------------------- UI helpers ----------------------
    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def make_button(self, parent, text, command, primary=True, width=None):
        bg = BLUE if primary else "#EEF2FF"
        fg = "#FFFFFF" if primary else BLUE
        active_bg = BLUE_DARK if primary else "#DFE6FF"
        btn = tk.Button(
            parent, text=text, command=command,
            bg=bg, fg=fg, activebackground=active_bg,
            activeforeground=fg, relief="flat", bd=0,
            cursor="hand2", font=(FONT, 10, "bold"),
            padx=17, pady=11, width=width
        )
        btn.bind("<Enter>", lambda e: btn.configure(bg=active_bg))
        btn.bind("<Leave>", lambda e: btn.configure(bg=bg))
        return btn

    def card(self, parent, padding=22):
        frame = tk.Frame(parent, bg=CARD, highlightbackground=BORDER,
                         highlightthickness=1, bd=0)
        frame.configure(padx=padding, pady=padding)
        return frame

    def label(self, parent, text, size=10, color=NAVY, bold=False, **kwargs):
        return tk.Label(
            parent, text=text, bg=kwargs.pop("bg", parent.cget("bg")),
            fg=color, font=(FONT, size, "bold" if bold else "normal"),
            **kwargs
        )

    def page_heading(self, parent, title, subtitle):
        self.label(parent, title, 23, NAVY, True).pack(anchor="w")
        self.label(parent, subtitle, 10, MUTED).pack(anchor="w", pady=(5, 20))

    def field_label(self, parent, text):
        self.label(parent, text, 10, "#526078", True).pack(anchor="w", pady=(12, 6))

    def create_entry(self, parent, variable=None, show=None):
        entry = tk.Entry(
            parent, textvariable=variable, show=show,
            font=(FONT, 11), bg="#F8FAFD", fg=NAVY,
            insertbackground=BLUE, relief="flat",
            highlightthickness=1, highlightbackground=BORDER,
            highlightcolor=BLUE
        )
        entry.pack(fill="x", ipady=11, padx=1)
        return entry

    def create_combo(self, parent, values, variable=None):
        combo = ttk.Combobox(
            parent, values=values, textvariable=variable,
            state="readonly", style="Modern.TCombobox", font=(FONT, 10)
        )
        combo.pack(fill="x")
        return combo

    # ---------------------- Login ----------------------
    def show_login(self):
        self.clear_root()
        outer = tk.Frame(self.root, bg=BG)
        outer.pack(fill="both", expand=True)

        left = tk.Frame(outer, bg=NAVY, width=440)
        left.pack(side="left", fill="both")
        left.pack_propagate(False)

        brand = tk.Frame(left, bg=NAVY)
        brand.pack(anchor="nw", padx=42, pady=38)
        logo = tk.Label(brand, text="✚", bg=BLUE, fg="white",
                        font=(FONT, 19, "bold"), width=2, height=1)
        logo.pack(side="left", padx=(0, 10))
        tk.Label(brand, text="clinic queue", bg=NAVY, fg="white",
                 font=(FONT, 17, "bold")).pack(side="left")

        art = tk.Frame(left, bg="#22345B", width=310, height=250)
        art.pack(padx=42, pady=(75, 25), fill="x")
        art.pack_propagate(False)
        tk.Label(art, text="✚", bg="#22345B", fg="#75E3D5",
                 font=(FONT, 60, "bold")).pack(pady=(24, 0))
        tk.Label(art, text="Antrean lebih tertata,\nkunjungan lebih nyaman.",
                 bg="#22345B", fg="white", font=(FONT, 17, "bold"),
                 justify="center").pack(pady=10)
        tk.Label(left, text="Sistem antrean klinik digital\nCepat • Praktis • Terorganisir",
                 bg=NAVY, fg="#B7C5E3", font=(FONT, 10),
                 justify="left").pack(anchor="w", padx=42, pady=12)

        right = tk.Frame(outer, bg=BG)
        right.pack(side="left", fill="both", expand=True)
        form = tk.Frame(right, bg=BG, width=390)
        form.place(relx=0.5, rely=0.5, anchor="center", width=390)

        self.label(form, "Selamat datang 👋", 25, NAVY, True, bg=BG).pack(anchor="w")
        self.label(form, "Masuk untuk mengatur kunjungan kesehatanmu.",
                   10, MUTED, bg=BG).pack(anchor="w", pady=(8, 26))

        self.field_label(form, "NIM / ID Pengguna")
        self.login_nim = tk.StringVar()
        nim_entry = self.create_entry(form, self.login_nim)
        nim_entry.insert(0, "")
        nim_entry.focus_set()

        self.field_label(form, "Nama lengkap")
        self.login_name = tk.StringVar()
        self.create_entry(form, self.login_name)

        tk.Label(form, text="Gunakan NIM sebagai identitas login.",
                 bg=BG, fg=MUTED, font=(FONT, 9)).pack(anchor="w", pady=(8, 18))
        self.make_button(form, "Masuk ke Dashboard  →", self.do_login).pack(fill="x")
        tk.Label(form, text="Demo akademik • Data disimpan selama aplikasi berjalan",
                 bg=BG, fg="#9AA5B7", font=(FONT, 8)).pack(anchor="w", pady=(25, 0))

    def do_login(self):
        nim = self.login_nim.get().strip()
        name = self.login_name.get().strip()
        if not nim or not name:
            messagebox.showwarning("Data belum lengkap",
                                   "Masukkan NIM dan nama lengkap terlebih dahulu.")
            return
        self.user_nim = nim
        self.user_name = name
        self.show_app()

    # ---------------------- Main shell ----------------------
    def show_app(self):
        self.clear_root()
        shell = tk.Frame(self.root, bg=BG)
        shell.pack(fill="both", expand=True)

        sidebar = tk.Frame(shell, bg="#FFFFFF", width=225,
                           highlightbackground=BORDER, highlightthickness=1)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        brand = tk.Frame(sidebar, bg="#FFFFFF")
        brand.pack(fill="x", padx=20, pady=(25, 28))
        tk.Label(brand, text="✚", bg=BLUE, fg="white", width=2,
                 font=(FONT, 15, "bold"), pady=5).pack(side="left", padx=(0, 9))
        tk.Label(brand, text="clinic queue", bg="#FFFFFF", fg=NAVY,
                 font=(FONT, 14, "bold")).pack(side="left")

        tk.Label(sidebar, text="MENU UTAMA", bg="#FFFFFF", fg="#9AA5B7",
                 font=(FONT, 8, "bold")).pack(anchor="w", padx=22, pady=(0, 9))

        self.nav_buttons = {}
        nav_items = [
            ("⌂", "Beranda"),
            ("＋", "Daftar Antrean"),
            ("≋", "Cek Antrean"),
            ("◉", "Profil Saya"),
        ]
        for icon, name in nav_items:
            btn = tk.Button(
                sidebar, text=f"  {icon}    {name}", anchor="w",
                command=lambda n=name: self.navigate(n),
                relief="flat", bd=0, cursor="hand2",
                font=(FONT, 10, "bold" if name == self.current_page else "normal"),
                padx=15, pady=13
            )
            btn.pack(fill="x", padx=12, pady=3)
            self.nav_buttons[name] = btn

        spacer = tk.Frame(sidebar, bg="#FFFFFF")
        spacer.pack(fill="both", expand=True)
        userbox = tk.Frame(sidebar, bg="#F5F7FC", padx=12, pady=12)
        userbox.pack(fill="x", padx=12, pady=(0, 10))
        tk.Label(userbox, text="●", fg=TEAL, bg="#F5F7FC",
                 font=(FONT, 16)).pack(side="left", padx=(0, 8))
        usertext = tk.Frame(userbox, bg="#F5F7FC")
        usertext.pack(side="left", fill="x", expand=True)
        tk.Label(usertext, text=self.user_name, bg="#F5F7FC", fg=NAVY,
                 font=(FONT, 9, "bold"), anchor="w").pack(fill="x")
        tk.Label(usertext, text=self.user_nim, bg="#F5F7FC", fg=MUTED,
                 font=(FONT, 8), anchor="w").pack(fill="x")
        self.make_button(sidebar, "↪  Keluar", self.logout, primary=False).pack(
            fill="x", padx=12, pady=(0, 18)
        )

        main = tk.Frame(shell, bg=BG)
        main.pack(side="left", fill="both", expand=True)
        header = tk.Frame(main, bg="#FFFFFF", height=66,
                          highlightbackground=BORDER, highlightthickness=1)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="Portal Layanan Kesehatan", bg="#FFFFFF",
                 fg=NAVY, font=(FONT, 11, "bold")).pack(side="left", padx=28)
        tk.Label(header, text=datetime.now().strftime("%d %b %Y"),
                 bg="#FFFFFF", fg=MUTED, font=(FONT, 9)).pack(side="right", padx=28)

        self.content = tk.Frame(main, bg=BG)
        self.content.pack(fill="both", expand=True, padx=28, pady=25)
        self.navigate(self.current_page)

    def navigate(self, page):
        self.current_page = page
        for name, btn in self.nav_buttons.items():
            active = name == page
            btn.configure(
                bg="#EAF0FF" if active else "#FFFFFF",
                fg=BLUE if active else "#66738A",
                font=(FONT, 10, "bold" if active else "normal")
            )
        for widget in self.content.winfo_children():
            widget.destroy()

        if page == "Beranda":
            self.page_home()
        elif page == "Daftar Antrean":
            self.page_register()
        elif page == "Cek Antrean":
            self.page_check()
        elif page == "Profil Saya":
            self.page_profile()

    def logout(self):
        if messagebox.askyesno("Keluar", "Yakin ingin keluar dari akun ini?"):
            self.user_nim = ""
            self.user_name = ""
            self.current_page = "Beranda"
            self.show_login()

    # ---------------------- Dashboard ----------------------
    def page_home(self):
        self.page_heading(
            self.content, f"Halo, {self.user_name.split()[0]}! 👋",
            "Selamat datang kembali. Yuk, atur kunjungan kesehatanmu."
        )

        banner = tk.Frame(self.content, bg=NAVY, padx=25, pady=22)
        banner.pack(fill="x", pady=(0, 18))
        left = tk.Frame(banner, bg=NAVY)
        left.pack(side="left", fill="both", expand=True)
        tk.Label(left, text="Kesehatan dimulai dari langkah kecil.",
                 bg=NAVY, fg="#FFFFFF", font=(FONT, 17, "bold")).pack(anchor="w")
        tk.Label(left, text="Daftar antrean lebih awal agar kunjungan lebih terencana.",
                 bg=NAVY, fg="#C5D1EA", font=(FONT, 10)).pack(anchor="w", pady=(8, 16))
        self.make_button(left, "Daftar Antrean  →",
                         lambda: self.navigate("Daftar Antrean")).pack(anchor="w")
        tk.Label(banner, text="✚", bg=NAVY, fg="#75E3D5",
                 font=(FONT, 58, "bold")).pack(side="right", padx=20)

        stats = tk.Frame(self.content, bg=BG)
        stats.pack(fill="x", pady=(0, 18))
        for col in range(3):
            stats.columnconfigure(col, weight=1, uniform="stats")
        active_count = len([b for b in self.bookings if b["status"] == "Terdaftar"])
        stat_data = [
            ("Total Pendaftaran", str(len(self.bookings)), "▣", BLUE),
            ("Antrean Aktif", str(active_count), "≋", TEAL),
            ("Status Akun", "Aktif", "✓", GREEN),
        ]
        for i, (title, value, icon, color) in enumerate(stat_data):
            box = self.card(stats, 17)
            box.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 8, 8 if i < 2 else 0))
            top = tk.Frame(box, bg=CARD)
            top.pack(fill="x")
            tk.Label(top, text=icon, bg="#EEF2FF", fg=color,
                     font=(FONT, 15, "bold"), width=3, pady=6).pack(side="left")
            tk.Label(box, text=title, bg=CARD, fg=MUTED,
                     font=(FONT, 9)).pack(anchor="w", pady=(13, 4))
            tk.Label(box, text=value, bg=CARD, fg=NAVY,
                     font=(FONT, 22, "bold")).pack(anchor="w")

        lower = tk.Frame(self.content, bg=BG)
        lower.pack(fill="both", expand=True)
        lower.columnconfigure(0, weight=3)
        lower.columnconfigure(1, weight=2)

        recent = self.card(lower, 18)
        recent.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        tk.Label(recent, text="Pendaftaran Terbaru", bg=CARD, fg=NAVY,
                 font=(FONT, 12, "bold")).pack(anchor="w")
        tk.Label(recent, text="Ringkasan antrean yang kamu buat.",
                 bg=CARD, fg=MUTED, font=(FONT, 9)).pack(anchor="w", pady=(4, 12))
        if not self.bookings:
            tk.Label(recent, text="Belum ada pendaftaran.\nMulai dengan membuat antrean pertamamu.",
                     bg="#F8FAFD", fg=MUTED, font=(FONT, 10),
                     justify="left", padx=14, pady=20).pack(fill="x")
        else:
            for b in self.bookings[-3:][::-1]:
                row = tk.Frame(recent, bg="#F8FAFD", padx=12, pady=10)
                row.pack(fill="x", pady=4)
                tk.Label(row, text=b["faskes"], bg="#F8FAFD", fg=NAVY,
                         font=(FONT, 9, "bold")).pack(anchor="w")
                tk.Label(row, text=f'{b["poli"]} • {b["tanggal"]} • No. {b["nomor"]}',
                         bg="#F8FAFD", fg=MUTED, font=(FONT, 8)).pack(anchor="w", pady=(3, 0))

        tips = self.card(lower, 18)
        tips.grid(row=0, column=1, sticky="nsew")
        tk.Label(tips, text="Panduan Singkat ✨", bg=CARD, fg=NAVY,
                 font=(FONT, 12, "bold")).pack(anchor="w", pady=(0, 12))
        for number, title, desc in [
            ("01", "Pilih fasilitas", "Tentukan klinik atau puskesmas."),
            ("02", "Pilih jadwal", "Sesuaikan hari dan waktu kunjungan."),
            ("03", "Simpan konfirmasi", "Periksa nomor antrean sebelum datang.")
        ]:
            item = tk.Frame(tips, bg=CARD)
            item.pack(fill="x", pady=7)
            tk.Label(item, text=number, bg="#EAF0FF", fg=BLUE,
                     font=(FONT, 9, "bold"), padx=9, pady=7).pack(side="left", padx=(0, 10))
            textframe = tk.Frame(item, bg=CARD)
            textframe.pack(side="left", fill="x", expand=True)
            tk.Label(textframe, text=title, bg=CARD, fg=NAVY,
                     font=(FONT, 9, "bold")).pack(anchor="w")
            tk.Label(textframe, text=desc, bg=CARD, fg=MUTED,
                     font=(FONT, 8), wraplength=190, justify="left").pack(anchor="w", pady=(2, 0))

    # ---------------------- Registration ----------------------
    def page_register(self):
        self.page_heading(
            self.content, "Daftar Antrean",
            "Lengkapi detail kunjungan, lalu periksa kembali sebelum konfirmasi."
        )

        body = tk.Frame(self.content, bg=BG)
        body.pack(fill="both", expand=True)
        body.columnconfigure(0, weight=3)
        body.columnconfigure(1, weight=2)

        form = self.card(body, 23)
        form.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        tk.Label(form, text="Detail kunjungan", bg=CARD, fg=NAVY,
                 font=(FONT, 13, "bold")).pack(anchor="w")
        tk.Label(form, text="Tanda * menunjukkan data yang wajib dipilih.",
                 bg=CARD, fg=MUTED, font=(FONT, 9)).pack(anchor="w", pady=(4, 8))

        self.faskes_var = tk.StringVar(value=list(self.faskes_data.keys())[0])
        self.poli_var = tk.StringVar()
        self.dokter_var = tk.StringVar()
        self.tanggal_var = tk.StringVar(value=(date.today() + timedelta(days=1)).isoformat())
        self.waktu_var = tk.StringVar(value="09:00")

        self.field_label(form, "Fasilitas kesehatan *")
        self.faskes_combo = self.create_combo(form, list(self.faskes_data.keys()), self.faskes_var)
        self.faskes_combo.bind("<<ComboboxSelected>>", self.update_clinic_options)

        self.field_label(form, "Poli tujuan *")
        self.poli_combo = self.create_combo(form, [], self.poli_var)

        self.field_label(form, "Dokter *")
        self.dokter_combo = self.create_combo(form, [], self.dokter_var)

        row = tk.Frame(form, bg=CARD)
        row.pack(fill="x")
        col1 = tk.Frame(row, bg=CARD)
        col1.pack(side="left", fill="x", expand=True, padx=(0, 8))
        col2 = tk.Frame(row, bg=CARD)
        col2.pack(side="left", fill="x", expand=True, padx=(8, 0))
        self.field_label(col1, "Tanggal (YYYY-MM-DD) *")
        self.create_entry(col1, self.tanggal_var)
        self.field_label(col2, "Waktu kunjungan *")
        self.waktu_combo = self.create_combo(
            col2, ["08:00", "09:00", "10:00", "11:00", "13:00", "14:00", "15:00"],
            self.waktu_var
        )
        self.update_clinic_options()

        self.make_button(form, "Periksa & Konfirmasi  →", self.confirm_booking).pack(
            fill="x", pady=(22, 0)
        )

        info = self.card(body, 22)
        info.grid(row=0, column=1, sticky="nsew")
        tk.Label(info, text="Sebelum mendaftar", bg=CARD, fg=NAVY,
                 font=(FONT, 13, "bold")).pack(anchor="w")
        tk.Label(info, text="Pastikan jadwal sesuai rencana kunjunganmu.",
                 bg=CARD, fg=MUTED, font=(FONT, 9), wraplength=230,
                 justify="left").pack(anchor="w", pady=(6, 18))
        for icon, title, desc in [
            ("✓", "Tanggal valid", "Tanggal tidak boleh sebelum hari ini."),
            ("◷", "Jadwal tersedia", "Satu slot waktu dibatasi untuk simulasi."),
            ("▣", "Konfirmasi tersimpan", "Nomor antrean muncul setelah pendaftaran berhasil.")
        ]:
            row = tk.Frame(info, bg="#F7F9FD", padx=12, pady=12)
            row.pack(fill="x", pady=5)
            tk.Label(row, text=icon, bg="#E6FAF5", fg=TEAL,
                     font=(FONT, 14, "bold"), width=2).pack(side="left", padx=(0, 9))
            textframe = tk.Frame(row, bg="#F7F9FD")
            textframe.pack(side="left", fill="x", expand=True)
            tk.Label(textframe, text=title, bg="#F7F9FD", fg=NAVY,
                     font=(FONT, 9, "bold")).pack(anchor="w")
            tk.Label(textframe, text=desc, bg="#F7F9FD", fg=MUTED,
                     font=(FONT, 8), wraplength=175, justify="left").pack(anchor="w", pady=(3, 0))

    def update_clinic_options(self, event=None):
        data = self.faskes_data.get(self.faskes_var.get(), {})
        polis = data.get("poli", [])
        doctors = data.get("dokter", [])
        self.poli_combo.configure(values=polis)
        self.dokter_combo.configure(values=doctors)
        if polis and self.poli_var.get() not in polis:
            self.poli_var.set(polis[0])
        if doctors and self.dokter_var.get() not in doctors:
            self.dokter_var.set(doctors[0])

    def confirm_booking(self):
        faskes = self.faskes_var.get()
        poli = self.poli_var.get()
        dokter = self.dokter_var.get()
        tanggal_text = self.tanggal_var.get().strip()
        waktu = self.waktu_var.get()

        if not all([faskes, poli, dokter, tanggal_text, waktu]):
            messagebox.showwarning("Data belum lengkap", "Lengkapi semua pilihan terlebih dahulu.")
            return
        try:
            tanggal_obj = datetime.strptime(tanggal_text, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Format tanggal salah", "Gunakan format YYYY-MM-DD, contoh 2026-10-20.")
            return
        if tanggal_obj < date.today():
            messagebox.showerror("Tanggal tidak valid", "Tanggal kunjungan tidak boleh sebelum hari ini.")
            return

        # Slot dianggap penuh jika faskes, dokter, tanggal, dan waktu sama.
        occupied = any(
            b["faskes"] == faskes and b["dokter"] == dokter
            and b["tanggal"] == tanggal_text and b["waktu"] == waktu
            for b in self.bookings
        )
        if occupied:
            messagebox.showerror("Jadwal tidak tersedia",
                                 "Slot dokter pada waktu tersebut sudah terdaftar. Silakan pilih waktu lain.")
            return

        nomor = 1 + sum(
            1 for b in self.bookings
            if b["faskes"] == faskes and b["dokter"] == dokter
            and b["tanggal"] == tanggal_text
        )
        booking = {
            "id": f"CQ-{random.randint(1000, 9999)}",
            "faskes": faskes,
            "poli": poli,
            "dokter": dokter,
            "tanggal": tanggal_text,
            "waktu": waktu,
            "nomor": nomor,
            "status": "Terdaftar",
            "pemilik": self.user_nim
        }
        self.bookings.append(booking)
        self.selected_booking = booking

        messagebox.showinfo(
            "Pendaftaran berhasil 🎉",
            f"Antrean berhasil dibuat!\n\n"
            f"Nomor antrean : {nomor:02d}\n"
            f"Fasilitas      : {faskes}\n"
            f"Poli           : {poli}\n"
            f"Dokter         : {dokter}\n"
            f"Tanggal        : {tanggal_text}\n"
            f"Waktu          : {waktu}\n\n"
            "Simpan detail ini dan datang sesuai jadwal."
        )
        self.navigate("Cek Antrean")

    # ---------------------- Queue check ----------------------
    def page_check(self):
        self.page_heading(
            self.content, "Cek Antrean",
            "Pantau status pendaftaran dan perkiraan antreanmu."
        )
        if not self.bookings:
            empty = self.card(self.content, 30)
            empty.pack(fill="x")
            tk.Label(empty, text="▤", bg=CARD, fg=BLUE,
                     font=(FONT, 34, "bold")).pack(anchor="w")
            tk.Label(empty, text="Belum ada antrean aktif", bg=CARD, fg=NAVY,
                     font=(FONT, 15, "bold")).pack(anchor="w", pady=(8, 5))
            tk.Label(empty, text="Buat pendaftaran terlebih dahulu untuk melihat nomor dan estimasi antrean.",
                     bg=CARD, fg=MUTED, font=(FONT, 10)).pack(anchor="w", pady=(0, 18))
            self.make_button(empty, "Buat Antrean", lambda: self.navigate("Daftar Antrean")).pack(anchor="w")
            return

        top = tk.Frame(self.content, bg=BG)
        top.pack(fill="x", pady=(0, 15))
        for b in self.bookings:
            self.draw_booking_card(top, b)

        table_card = self.card(self.content, 16)
        table_card.pack(fill="both", expand=True)
        tk.Label(table_card, text="Riwayat pendaftaran", bg=CARD, fg=NAVY,
                 font=(FONT, 12, "bold")).pack(anchor="w", pady=(0, 12))
        columns = ("nomor", "faskes", "poli", "tanggal", "waktu", "status")
        tree = ttk.Treeview(table_card, columns=columns, show="headings",
                            style="Modern.Treeview", height=5)
        headers = {
            "nomor": "No. Antrean", "faskes": "Fasilitas",
            "poli": "Poli", "tanggal": "Tanggal", "waktu": "Waktu", "status": "Status"
        }
        widths = {"nomor": 95, "faskes": 200, "poli": 120, "tanggal": 105, "waktu": 75, "status": 100}
        for col in columns:
            tree.heading(col, text=headers[col])
            tree.column(col, width=widths[col], anchor="w")
        for b in self.bookings[::-1]:
            tree.insert("", "end", values=(
                f'{b["nomor"]:02d}', b["faskes"], b["poli"],
                b["tanggal"], b["waktu"], b["status"]
            ))
        tree.pack(fill="both", expand=True)

    def draw_booking_card(self, parent, booking):
        card = self.card(parent, 20)
        card.pack(fill="x", pady=(0, 12))
        head = tk.Frame(card, bg=CARD)
        head.pack(fill="x")
        tk.Label(head, text=booking["faskes"], bg=CARD, fg=NAVY,
                 font=(FONT, 12, "bold")).pack(side="left")
        tk.Label(head, text="●  TERDAFTAR", bg="#E6FAF2", fg=GREEN,
                 font=(FONT, 8, "bold"), padx=10, pady=6).pack(side="right")

        detail = tk.Frame(card, bg=CARD)
        detail.pack(fill="x", pady=(16, 8))
        for col in range(4):
            detail.columnconfigure(col, weight=1)
        info = [
            ("NOMOR ANTREAN", f'{booking["nomor"]:02d}'),
            ("POLI", booking["poli"]),
            ("TANGGAL", booking["tanggal"]),
            ("JADWAL", booking["waktu"])
        ]
        for i, (label, value) in enumerate(info):
            tk.Label(detail, text=label, bg=CARD, fg=MUTED,
                     font=(FONT, 8, "bold")).grid(row=0, column=i, sticky="w", padx=(0, 10))
            tk.Label(detail, text=value, bg=CARD, fg=BLUE if i == 0 else NAVY,
                     font=(FONT, 12 if i == 0 else 10, "bold")).grid(
                         row=1, column=i, sticky="w", padx=(0, 10), pady=(6, 0))
        queue_ahead = max(0, (booking["nomor"] - 1) * 3)
        tk.Label(card, text=f'Perkiraan antrean di depan: {booking["nomor"] - 1} orang  •  '
                            f'Estimasi tunggu: sekitar {queue_ahead} menit',
                 bg="#F3F6FF", fg="#4B5E91", font=(FONT, 9),
                 padx=12, pady=10, anchor="w").pack(fill="x", pady=(10, 0))
        tk.Label(card, text=f'Dokter: {booking["dokter"]}   •   ID: {booking["id"]}',
                 bg=CARD, fg=MUTED, font=(FONT, 8)).pack(anchor="w", pady=(10, 0))

    # ---------------------- Profile ----------------------
    def page_profile(self):
        self.page_heading(
            self.content, "Profil Saya",
            "Informasi pengguna yang sedang masuk ke sistem."
        )
        profile = self.card(self.content, 28)
        profile.pack(fill="x")
        top = tk.Frame(profile, bg=CARD)
        top.pack(fill="x", pady=(0, 22))
        tk.Label(top, text="●", bg="#EAF0FF", fg=BLUE,
                 font=(FONT, 32, "bold"), width=3, pady=8).pack(side="left", padx=(0, 16))
        textframe = tk.Frame(top, bg=CARD)
        textframe.pack(side="left", fill="x", expand=True)
        tk.Label(textframe, text=self.user_name, bg=CARD, fg=NAVY,
                 font=(FONT, 18, "bold")).pack(anchor="w")
        tk.Label(textframe, text="Pengguna Clinic Queue", bg=CARD, fg=MUTED,
                 font=(FONT, 10)).pack(anchor="w", pady=(5, 0))
        tk.Frame(profile, bg=BORDER, height=1).pack(fill="x", pady=(0, 12))

        rows = [
            ("NIM / ID Pengguna", self.user_nim),
            ("Nama lengkap", self.user_name),
            ("Total pendaftaran", str(len(self.bookings))),
            ("Status akun", "Aktif selama sesi aplikasi")
        ]
        for label, value in rows:
            row = tk.Frame(profile, bg=CARD)
            row.pack(fill="x", pady=10)
            tk.Label(row, text=label, bg=CARD, fg=MUTED,
                     font=(FONT, 10)).pack(side="left")
            tk.Label(row, text=value, bg=CARD, fg=NAVY,
                     font=(FONT, 10, "bold")).pack(side="right")

        note = tk.Frame(self.content, bg="#FFF8E8", padx=16, pady=14)
        note.pack(fill="x", pady=16)
        tk.Label(note, text="Catatan demo", bg="#FFF8E8", fg="#946200",
                 font=(FONT, 9, "bold")).pack(anchor="w")
        tk.Label(note, text="Data pendaftaran tersimpan sementara selama aplikasi terbuka. "
                            "Aplikasi ini merupakan prototipe tugas dan belum terhubung ke server klinik.",
                 bg="#FFF8E8", fg="#8B6B2C", font=(FONT, 9),
                 wraplength=760, justify="left").pack(anchor="w", pady=(4, 0))


# ==========================================================
# FITUR TAMBAHAN: GRAFIK + PENGUNJUNG 24 JAM + FIREBASE
# Paste sebelum: if __name__ == "__main__":
# ==========================================================

import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta, date

# GANTI dengan URL Firebase Realtime Database milikmu.
# Contoh: https://nama-project-default-rtdb.firebaseio.com
FIREBASE_URL = "https://clinicqueue-90808-default-rtdb.firebaseio.com/"


def firebase_request(method, path, data=None):
    if not FIREBASE_URL.startswith("https://"):
        raise ValueError("URL Firebase belum diisi.")

    url = FIREBASE_URL.rstrip("/") + "/" + path + ".json"
    body = None if data is None else json.dumps(data).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method=method
    )

    with urllib.request.urlopen(req, timeout=8) as response:
        result = response.read().decode("utf-8")
        return json.loads(result) if result else None


# Simpan fungsi asli agar fitur lama tetap digunakan.
_asli_do_login = ClinicQueueApp.do_login
_asli_confirm_booking = ClinicQueueApp.confirm_booking
_asli_page_home = ClinicQueueApp.page_home
_asli_show_app = ClinicQueueApp.show_app


def gabung_booking(lokal, online):
    hasil = {b["id"]: b for b in lokal}

    if isinstance(online, dict):
        for b in online.values():
            if isinstance(b, dict) and "id" in b:
                if b["id"] not in hasil:
                    hasil[b["id"]] = b
                else:
                    hasil[b["id"]].update(b)

    return list(hasil.values())


def ambil_booking_online(self):
    data = firebase_request("GET", "bookings")
    gabungan = gabung_booking(self.bookings, data)

    berubah = {
        b["id"]: b for b in gabungan
    } != {
        b["id"]: b for b in self.bookings
    }

    self.bookings = gabungan
    return berubah


def simpan_booking_online(booking):
    # ID booking digunakan sebagai identitas unik.
    firebase_request("PUT", "bookings/" + booking["id"], booking)


def login_tambahan(self):
    _asli_do_login(self)

    # Lanjutkan hanya jika login berhasil masuk ke aplikasi.
    if self.user_nim:
        try:
            ambil_booking_online(self)
            self.navigate(self.current_page)
        except Exception as e:
            messagebox.showwarning(
                "Sinkronisasi",
                "Data online belum bisa diambil.\n"
                "Periksa URL Firebase dan koneksi internet.\n\n"
                + str(e)
            )

        if not getattr(self, "_sync_aktif", False):
            self._sync_aktif = True
            self.root.after(5000, lambda: sinkronisasi_otomatis(self))


def sinkronisasi_otomatis(self):
    if not self.root.winfo_exists():
        return

    try:
        berubah = ambil_booking_online(self)

        if berubah and self.user_nim:
            self.navigate(self.current_page)

    except Exception:
        # Jika internet terputus, coba lagi pada pemeriksaan berikutnya.
        pass

    self.root.after(5000, lambda: sinkronisasi_otomatis(self))


def konfirmasi_tambahan(self):
    id_sebelum = {b["id"] for b in self.bookings}

    # Jalankan proses pendaftaran asli.
    _asli_confirm_booking(self)

    booking_baru = [
        b for b in self.bookings if b["id"] not in id_sebelum
    ]

    for booking in booking_baru:
        booking["created_at"] = datetime.now().isoformat(
            timespec="seconds"
        )

        try:
            simpan_booking_online(booking)
        except Exception as e:
            messagebox.showwarning(
                "Data belum tersinkron",
                "Pendaftaran ada di perangkat ini, tetapi belum "
                "berhasil dikirim ke Firebase.\n"
                "Periksa koneksi internet dan URL Firebase.\n\n"
                + str(e)
            )


def grafik_tambahan(self):
    _asli_page_home(self)

    # Sisipkan grafik pada beranda tanpa mengganti komponen lama.
    anak = self.content.winfo_children()
    if not anak:
        return

    lower = anak[-1]

    wadah = tk.Frame(self.content, bg="#FFFFFF",
                     highlightbackground="#E6EBF2",
                     highlightthickness=1)
    wadah.pack(fill="x", before=lower, pady=(0, 15))

    tk.Label(
        wadah,
        text="Grafik Pengunjung Harian",
        bg="#FFFFFF",
        fg="#182544",
        font=("Segoe UI", 12, "bold")
    ).pack(anchor="w", padx=18, pady=(12, 2))

    tk.Label(
        wadah,
        text="Jumlah pendaftaran berdasarkan tanggal",
        bg="#FFFFFF",
        fg="#7B879D",
        font=("Segoe UI", 9)
    ).pack(anchor="w", padx=18)

    canvas = tk.Canvas(
        wadah, height=145, bg="#FFFFFF",
        highlightthickness=0
    )
    canvas.pack(fill="x", padx=12, pady=8)

    hari_ini = date.today()
    daftar_hari = [
        hari_ini - timedelta(days=i)
        for i in range(6, -1, -1)
    ]

    jumlah = {hari: 0 for hari in daftar_hari}

    for b in self.bookings:
        waktu = b.get("created_at")

        if waktu:
            try:
                tanggal_booking = datetime.fromisoformat(
                    waktu
                ).date()

                if tanggal_booking in jumlah:
                    jumlah[tanggal_booking] += 1
            except (ValueError, TypeError):
                pass

    # Grafik batang tujuh hari terakhir.
    lebar = max(canvas.winfo_width(), 500)
    tinggi = 145
    kiri, kanan = 35, lebar - 15
    dasar = 105
    tinggi_maks = 65

    nilai_maks = max(jumlah.values()) if jumlah else 0
    nilai_maks = max(nilai_maks, 1)

    canvas.create_line(
        kiri, dasar, kanan, dasar,
        fill="#E6EBF2"
    )

    ruang = (kanan - kiri) / 7
    for i, hari in enumerate(daftar_hari):
        x = kiri + ruang * (i + 0.5)
        nilai = jumlah[hari]
        tinggi_batang = nilai / nilai_maks * tinggi_maks

        canvas.create_rectangle(
            x - 12, dasar - tinggi_batang,
            x + 12, dasar,
            fill="#4263EB", outline=""
        )

        canvas.create_text(
            x, dasar - tinggi_batang - 10,
            text=str(nilai),
            fill="#182544",
            font=("Segoe UI", 9, "bold")
        )

        canvas.create_text(
            x, 123,
            text=hari.strftime("%d/%m"),
            fill="#7B879D",
            font=("Segoe UI", 8)
        )

    # Hitung pengunjung dalam jendela 24 jam terakhir.
    sekarang = datetime.now()
    batas = sekarang - timedelta(hours=24)
    pengunjung_24_jam = 0

    for b in self.bookings:
        waktu = b.get("created_at")
        if waktu:
            try:
                dibuat = datetime.fromisoformat(waktu)
                if batas <= dibuat <= sekarang:
                    pengunjung_24_jam += 1
            except (ValueError, TypeError):
                pass

    tk.Label(
        wadah,
        text=f"Pendaftaran dalam 24 jam terakhir: "
             f"{pengunjung_24_jam}",
        bg="#FFFFFF",
        fg="#4263EB",
        font=("Segoe UI", 10, "bold")
    ).pack(anchor="w", padx=18, pady=(0, 12))


# Aktifkan tambahan tanpa menghapus fungsi asli.
ClinicQueueApp.do_login = login_tambahan
ClinicQueueApp.confirm_booking = konfirmasi_tambahan
ClinicQueueApp.page_home = grafik_tambahan

if __name__ == "__main__":
    root = tk.Tk()
    app = ClinicQueueApp(root)
    root.mainloop()
