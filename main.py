import tkinter as tk
import sqlite3
from tkinter import messagebox


class CarDeliveryApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Car Delivery System")

        self.label_customer_name = tk.Label(master, text="Customer Name:")
        self.label_customer_name.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)

        self.entry_customer_name = tk.Entry(master)
        self.entry_customer_name.grid(row=0, column=1, padx=10, pady=5)

        self.label_customer_address = tk.Label(master, text="Customer Address:")
        self.label_customer_address.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)

        self.entry_customer_address = tk.Entry(master)
        self.entry_customer_address.grid(row=1, column=1, padx=10, pady=5)

        self.label_delivery_date = tk.Label(master, text="Delivery Date:")
        self.label_delivery_date.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)

        self.entry_delivery_date = tk.Entry(master)
        self.entry_delivery_date.grid(row=2, column=1, padx=10, pady=5)

        self.button_submit = tk.Button(master, text="Submit", command=self.submit)
        self.button_submit.grid(row=3, columnspan=2, padx=10, pady=10)

        self.button_order_history = tk.Button(master, text="Order History", command=self.show_order_history)
        self.button_order_history.grid(row=4, columnspan=2, padx=10, pady=5)

        self.button_track_order = tk.Button(master, text="Track Order", command=self.track_order)
        self.button_track_order.grid(row=5, columnspan=2, padx=10, pady=5)

        self.button_delete_order = tk.Button(master, text="Delete Order", command=self.delete_order)
        self.button_delete_order.grid(row=6, columnspan=2, padx=10, pady=5)

        self.listbox_deliveries = tk.Listbox(master)
        self.listbox_deliveries.grid(row=7, columnspan=2, padx=10, pady=5, sticky=tk.W + tk.E)

        # Connect to SQLite database
        self.conn = sqlite3.connect('car_delivery.db')
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS deliveries
                          (id INTEGER PRIMARY KEY,
                           customer_name TEXT,
                           customer_address TEXT,
                           delivery_date TEXT)''')
        self.conn.commit()

    def load_data(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM deliveries")
        rows = cursor.fetchall()
        for row in rows:
            self.listbox_deliveries.insert(tk.END,
                                           f"ID: {row[0]}, Name: {row[1]}, Address: {row[2]}, Delivery Date: {row[3]}")

    def submit(self):
        customer_name = self.entry_customer_name.get()
        customer_address = self.entry_customer_address.get()
        delivery_date = self.entry_delivery_date.get()

        if customer_name and customer_address and delivery_date:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO deliveries (customer_name, customer_address, delivery_date) VALUES (?, ?, ?)",
                           (customer_name, customer_address, delivery_date))
            self.conn.commit()

            self.listbox_deliveries.insert(tk.END,
                                           f"Name: {customer_name}, Address: {customer_address}, Delivery Date: {delivery_date}")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def show_order_history(self):
        self.listbox_deliveries.delete(0, tk.END)
        self.load_data()

    def track_order(self):
        selected_item = self.listbox_deliveries.curselection()
        if selected_item:
            index = int(selected_item[0])
            order_id = self.listbox_deliveries.get(index).split(",")[0].split(":")[1].strip()
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM deliveries WHERE id=?", (order_id,))
            row = cursor.fetchone()
            if row:
                messagebox.showinfo("Order Details",
                                    f"ID: {row[0]}\nName: {row[1]}\nAddress: {row[2]}\nDelivery Date: {row[3]}")
            else:
                messagebox.showerror("Error", "Order not found.")
        else:
            messagebox.showerror("Error", "Please select an order from the list.")

    def delete_order(self):
        selected_item = self.listbox_deliveries.curselection()
        if selected_item:
            index = int(selected_item[0])
            order_id = self.listbox_deliveries.get(index).split(",")[0].split(":")[1].strip()
            if messagebox.askyesno("Delete Order", "Are you sure you want to delete this order?"):
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM deliveries WHERE id=?", (order_id,))
                self.conn.commit()
                self.listbox_deliveries.delete(index)
                messagebox.showinfo("Success", "Order deleted successfully.")
        else:
            messagebox.showerror("Error", "Please select an order from the list.")


def main():
    root = tk.Tk()
    app = CarDeliveryApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
