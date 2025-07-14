import tkinter as tk
from tkinter import filedialog, messagebox, font
import os
from pdf_utils import merge_pdfs, split_pdf, encrypt_pdf
import subprocess
import sys
from tkinter import ttk


class PDFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📎 PDF Automation Tool")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f4f8")

        self.custom_font = font.Font(family="Segoe UI", size=12)

        title = tk.Label(root, text="PDF Automation Tool", font=("Segoe UI", 20, "bold"), bg="#f0f4f8", fg="#2c3e50")
        title.pack(pady=20)

        btn_frame = tk.Frame(root, bg="#f0f4f8")
        btn_frame.pack(pady=30)

        self.make_button(btn_frame, "📎 Merge PDFs", self.merge_gui).pack(pady=10)
        self.make_button(btn_frame, "✂️ Split PDF", self.split_gui).pack(pady=10)
        self.make_button(btn_frame, "🔐 Encrypt PDF", self.encrypt_gui).pack(pady=10)

    def make_button(self, parent, text, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            width=30,
            height=2,
            font=self.custom_font,
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            relief="raised",
            bd=3
        )

    def center_window(self, win, width, height, offset=0):
        self.root.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (width // 2) + offset
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (height // 2) + offset
        win.geometry(f"{width}x{height}+{x}+{y}")
        win.lift()
        win.focus_force()
        win.transient(self.root)

    def show_progress(self, message="Processing..."):
        self.progress_win = tk.Toplevel(self.root)
        self.progress_win.title("Please Wait")
        self.center_window(self.progress_win, 400, 140, offset=40)
        self.progress_win.configure(bg="#f0f4f8")
        tk.Label(self.progress_win, text=message, bg="#f0f4f8", font=("Segoe UI", 12)).pack(pady=15)
        self.progress_bar = ttk.Progressbar(self.progress_win, mode='indeterminate')
        self.progress_bar.pack(pady=10, fill='x', padx=30)
        self.progress_bar.start(10)
        self.progress_win.grab_set()
        self.progress_win.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable close
        self.root.update()

    def hide_progress(self):
        if hasattr(self, 'progress_win') and self.progress_win:
            self.progress_bar.stop()
            self.progress_win.destroy()
            self.progress_win = None

    def merge_gui(self):
        paths = []

        def select_next():
            self.root.lift()
            self.root.focus_force()
            file = filedialog.askopenfilename(title="Select a PDF", filetypes=[("PDF Files", "*.pdf")], parent=self.root)
            if file:
                paths.append(file)
                update_list()

        def update_list():
            listbox.delete(0, tk.END)
            for idx, path in enumerate(paths):
                listbox.insert(tk.END, f"{idx+1}. {os.path.basename(path)}")

        def finish_merge():
            if len(paths) < 2:
                messagebox.showwarning("Not Enough Files", "Please select at least two PDFs to merge.", parent=win)
                return
            self.root.lift()
            self.root.focus_force()
            output_name = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF File", "*.pdf")],
                title="Save Merged PDF",
                parent=self.root
            )

            if output_name:
                if not output_name.lower().endswith(".pdf"):
                    output_name += ".pdf"
                try:
                    self.show_progress("Merging PDFs...")
                    self.root.after(100, lambda: self._merge_pdfs_async(paths, output_name, win))
                except Exception as e:
                    self.hide_progress()
                    messagebox.showerror("Error", f"Failed to merge PDFs:\n{e}")

        win = tk.Toplevel(self.root)
        win.title("Merge PDFs")
        self.center_window(win, 500, 450)
        win.configure(bg="#f7f7f7")

        tk.Label(win, text="Add PDFs one by one", font=("Segoe UI", 12), bg="#f7f7f7").pack(pady=10)

        listbox = tk.Listbox(win, width=50, height=10)
        listbox.pack(pady=10)

        tk.Button(win, text="➕ Add Another PDF", command=select_next, bg="#3498db", fg="white").pack(pady=5)
        tk.Button(win, text="✅ Merge Files", command=finish_merge, bg="#2ecc71", fg="white").pack(pady=10)

    def _merge_pdfs_async(self, paths, output_name, win):
        try:
            result = merge_pdfs(paths, output_name)
            self.hide_progress()
            self.show_success_with_open(result)
            win.destroy()
        except Exception as e:
            self.hide_progress()
            messagebox.showerror("Error", f"Failed to merge PDFs:\n{e}")

    def split_gui(self):
        self.root.lift()
        self.root.focus_force()
        path = filedialog.askopenfilename(title="Select PDF to Split", filetypes=[("PDF Files", "*.pdf")], parent=self.root)
        if path:
            win = tk.Toplevel(self.root)
            win.title("Split PDF")
            self.center_window(win, 420, 300, offset=30)
            win.configure(bg="#f9f9f9")

            tk.Label(win, text="Start Page (0-based):", bg="#f9f9f9").pack(pady=5)
            start_entry = tk.Entry(win)
            start_entry.pack(pady=5)

            tk.Label(win, text="End Page:", bg="#f9f9f9").pack(pady=5)
            end_entry = tk.Entry(win)
            end_entry.pack(pady=5)

            def split_action():
                try:
                    start = int(start_entry.get())
                    end = int(end_entry.get())
                    self.root.lift()
                    self.root.focus_force()
                    output = filedialog.asksaveasfilename(
                        defaultextension=".pdf",
                        filetypes=[("PDF File", "*.pdf")],
                        title="Save Split PDF",
                        parent=self.root
                    )
                    if output:
                        self.show_progress("Splitting PDF...")
                        self.root.after(100, lambda: self._split_pdf_async(path, start, end, output, win))
                except Exception:
                    messagebox.showerror("Error", "Invalid input. Please enter valid page numbers.")

            tk.Button(win, text="Split", command=split_action, bg="#2ecc71", fg="white").pack(pady=10)

    def _split_pdf_async(self, path, start, end, output, win):
        try:
            result = split_pdf(path, start, end, output)
            self.hide_progress()
            self.show_success_with_open(result)
            win.destroy()
        except Exception as e:
            self.hide_progress()
            messagebox.showerror("Error", f"Failed to split PDF:\n{e}")

    def encrypt_gui(self):
        self.root.lift()
        self.root.focus_force()
        path = filedialog.askopenfilename(title="Select PDF to Encrypt", filetypes=[("PDF Files", "*.pdf")], parent=self.root)
        if path:
            win = tk.Toplevel(self.root)
            win.title("Encrypt PDF")
            self.center_window(win, 420, 250, offset=60)
            win.configure(bg="#f9f9f9")

            tk.Label(win, text="Enter Password:", bg="#f9f9f9").pack(pady=10)
            pass_entry = tk.Entry(win, show="*")
            pass_entry.pack(pady=5)

            def encrypt_action():
                password = pass_entry.get()
                self.root.lift()
                self.root.focus_force()
                output = filedialog.asksaveasfilename(
                    defaultextension=".pdf",
                    filetypes=[("PDF File", "*.pdf")],
                    title="Save Encrypted PDF",
                    parent=self.root
                )
                if output:
                    self.show_progress("Encrypting PDF...")
                    self.root.after(100, lambda: self._encrypt_pdf_async(path, password, output, win))

            tk.Button(win, text="Encrypt", command=encrypt_action, bg="#e67e22", fg="white").pack(pady=15)

    def _encrypt_pdf_async(self, path, password, output, win):
        try:
            result = encrypt_pdf(path, password, output)
            self.hide_progress()
            self.show_success_with_open(result)
            win.destroy()
        except Exception as e:
            self.hide_progress()
            messagebox.showerror("Error", f"Failed to encrypt PDF:\n{e}")

    def show_success_with_open(self, file_path):
        def open_output_dir():
            folder = os.path.dirname(file_path)
            if sys.platform.startswith('win'):
                os.startfile(folder)
            elif sys.platform.startswith('darwin'):
                subprocess.Popen(['open', folder])
            else:
                subprocess.Popen(['xdg-open', folder])
        win = tk.Toplevel(self.root)
        win.title("Success")
        self.center_window(win, 450, 200, offset=80)
        win.configure(bg="#f0f4f8")
        tk.Label(win, text=f"File saved at:\n{file_path}", bg="#f0f4f8", font=("Segoe UI", 11)).pack(pady=15)
        tk.Button(win, text="Open Output Folder", command=open_output_dir, bg="#3498db", fg="white").pack(pady=10)
        tk.Button(win, text="Close", command=win.destroy, bg="#2ecc71", fg="white").pack(pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFApp(root)
    root.mainloop()
