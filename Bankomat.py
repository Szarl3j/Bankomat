import tkinter as tk
from tkinter import simpledialog, messagebox

class ATM(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ATM")
        self.geometry("400x300")

        self.banknotes = {10: 10, 20: 10, 50: 10, 100: 10, 200: 10, 500: 10}

        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.banknote_status_area = tk.Text(main_frame, wrap=tk.WORD, height=10)
        self.banknote_status_area.pack(fill=tk.BOTH, expand=True)

        self.output_area = tk.Text(main_frame, wrap=tk.WORD, height=5)
        self.output_area.pack(fill=tk.BOTH, expand=True)

        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X)

        withdraw_button = tk.Button(button_frame, text="Withdraw", command=self.withdraw)
        withdraw_button.grid(row=0, column=0, padx=5, pady=5)

        admin_button = tk.Button(button_frame, text="Admin", command=self.open_admin_panel)
        admin_button.grid(row=0, column=1, padx=5, pady=5)

        self.update_banknote_status()

    def withdraw(self):
        amount_str = simpledialog.askstring("Withdraw", "Enter amount to withdraw:")
        if amount_str:
            try:
                amount = int(amount_str)
                if self.is_withdraw_possible(amount):
                    self.withdraw_amount(amount)
                    self.update_banknote_status()
                else:
                    messagebox.showerror("Error", f"Unable to dispense amount {amount} PLN.")
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter a valid number.")

    def withdraw_amount(self, amount):
        withdrawal = {}
        remaining_amount = amount

        for denomination in sorted(self.banknotes.keys(), reverse=True):
            banknotes_available = self.banknotes[denomination]
            banknotes_to_withdraw = min(remaining_amount // denomination, banknotes_available)

            if banknotes_to_withdraw > 0:
                withdrawal[denomination] = banknotes_to_withdraw
                remaining_amount -= banknotes_to_withdraw * denomination
                self.banknotes[denomination] -= banknotes_to_withdraw

        if remaining_amount == 0:
            self.output_area.insert(tk.END, f"Dispensed amount {amount} PLN with banknotes:\n")
            for denomination, count in withdrawal.items():
                self.output_area.insert(tk.END, f"{count} x {denomination} PLN\n")
        else:
            messagebox.showerror("Error", f"Unable to dispense amount {amount} PLN.")

    def is_withdraw_possible(self, amount):
        total_money = sum(denomination * count for denomination, count in self.banknotes.items())
        return total_money >= amount

    def open_admin_panel(self):
        AdminPanel(self)

    def update_banknote_status(self):
        self.banknote_status_area.delete(1.0, tk.END)
        self.banknote_status_area.insert(tk.END, "Banknote status:\n")
        for denomination, count in self.banknotes.items():
            self.banknote_status_area.insert(tk.END, f"{denomination} PLN: {count} banknotes\n")

class AdminPanel(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Admin Panel")
        self.geometry("300x200")

        self.banknotes = parent.banknotes

        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.entry_fields = {}
        for denomination, count in self.banknotes.items():
            label = tk.Label(main_frame, text=f"{denomination} PLN:")
            label.pack(side=tk.LEFT, padx=5, pady=5)

            entry = tk.Entry(main_frame)
            entry.insert(tk.END, count)
            entry.pack(side=tk.LEFT, padx=5, pady=5)
            self.entry_fields[denomination] = entry

        save_button = tk.Button(main_frame, text="Save", command=self.save_banknotes)
        save_button.pack(fill=tk.X, padx=5, pady=5)

    def save_banknotes(self):
        for denomination, entry in self.entry_fields.items():
            new_count = int(entry.get())
            self.banknotes[denomination] += new_count
        self.master.update_banknote_status()
        self.destroy()

if __name__ == "__main__":
    app = ATM()
    app.mainloop()

