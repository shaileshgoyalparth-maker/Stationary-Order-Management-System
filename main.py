import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class StationeryOrderManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("Stationery Order Management App")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.stationery_items = {
            "NOTEBOOK": 3,
            "PENCIL PACK(contains 10 pencils)": 10,
            "PEN SET(contains 5 blue and 5 black)": 20,
            "ERASER": 1,
            "GEOMETRY BOX": 6,
            "COLOUR PENCILS": 5,
            "ERASER PACK(contains 20 erasers)": 20,
            "LONG NOTEBOOK": 5,
            "WAX CRAYONS(contains 12 crayons)": 12,
            "PLASTIC CRAYONS(contains 12 crayons)": 12,
            "Plastic Ruler": 5,
            "Plastic Ruler Pack(contains 3 rulers)": 15,
            "Steel Ruler": 6,
            "Steel Ruler Pack(contains 3 rulers)": 18,
            "Water Colour Pack(contains 20 colours)": 40
        }

        self.exchange_rate = 82

        self.setup_background(root)

        frame = ttk.Frame(root)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        ttk.Label(
            frame,
            text="Stationery Order Management",
            font=("Arial", 20, "bold")
        ).grid(
            row=0,
            column=0,
            columnspan=4,
            padx=10,
            pady=10
        )

        self.item_labels = {}
        self.item_quantities = {}

        items = list(self.stationery_items.items())

        for index, (item, price) in enumerate(items):
            column = (index // 8) * 2
            row = (index % 8) + 1

            item_label = ttk.Label(
                frame,
                text=f"{item} (${price}):",
                font=("Arial", 9)
            )

            item_label.grid(
                row=row,
                column=column,
                padx=5,
                pady=5,
                sticky="w"
            )

            self.item_labels[item] = item_label

            quantity_entry = ttk.Entry(
                frame,
                width=5
            )

            quantity_entry.grid(
                row=row,
                column=column + 1,
                padx=5,
                pady=5
            )

            self.item_quantities[item] = quantity_entry

        self.currency_var = tk.StringVar(value="USD")

        ttk.Label(
            frame,
            text="Currency:",
            font=("Arial", 12)
        ).grid(
            row=9,
            column=0,
            padx=10,
            pady=10
        )

        currency_dropdown = ttk.Combobox(
            frame,
            textvariable=self.currency_var,
            state="readonly",
            width=18,
            values=("USD", "INR")
        )

        currency_dropdown.grid(
            row=9,
            column=1,
            padx=10,
            pady=10
        )

        self.currency_var.trace_add(
            "write",
            self.update_item_prices
        )

        order_button = ttk.Button(
            frame,
            text="Place Order",
            command=self.place_order
        )

        order_button.grid(
            row=10,
            column=0,
            columnspan=4,
            padx=10,
            pady=5
        )

        refresh_button = ttk.Button(
            frame,
            text="Refresh Order",
            command=self.refresh_order
        )

        refresh_button.grid(
            row=11,
            column=0,
            columnspan=4,
            padx=10,
            pady=5
        )

    def setup_background(self, root):
        background_width = 800
        background_height = 600

        try:
            original_image = Image.open("background.jpg")

            original_image = original_image.resize(
                (background_width, background_height),
                Image.Resampling.LANCZOS
            )

            background_image = ImageTk.PhotoImage(
                original_image
            )

            canvas = tk.Canvas(
                root,
                width=background_width,
                height=background_height,
                highlightthickness=0
            )

            canvas.place(x=0, y=0)

            canvas.create_image(
                0,
                0,
                anchor=tk.NW,
                image=background_image
            )

            canvas.image = background_image

        except Exception as e:
            messagebox.showerror(
                "Background Error",
                f"Unable to load background.jpg:\n{e}"
            )

    def update_item_prices(self, *args):
        currency = self.currency_var.get()

        symbol = "₹" if currency == "INR" else "$"

        rate = self.exchange_rate if currency == "INR" else 1

        for item, label in self.item_labels.items():

            price = self.stationery_items[item] * rate

            label.config(
                text=f"{item} ({symbol}{price}):"
            )

    def place_order(self):
        total_cost = 0

        order_summary = "Stationery Order Summary:\n"

        currency = self.currency_var.get()

        symbol = "₹" if currency == "INR" else "$"

        rate = self.exchange_rate if currency == "INR" else 1

        for item, entry in self.item_quantities.items():

            quantity_text = entry.get().strip()

            if quantity_text == "":
                continue

            if not quantity_text.isdigit():
                messagebox.showerror(
                    "Invalid Quantity",
                    f"Please enter a valid quantity for {item}."
                )
                return

            quantity = int(quantity_text)

            if quantity > 0:

                price = self.stationery_items[item] * rate

                cost = quantity * price

                total_cost += cost

                order_summary += (
                    f"{item}: {quantity} x "
                    f"{symbol}{price} = {symbol}{cost}\n"
                )

        if total_cost > 0:

            order_summary += (
                f"\nTotal Cost: {symbol}{total_cost}"
            )

            messagebox.showinfo(
                "Order Placed",
                order_summary
            )

        else:

            messagebox.showerror(
                "Error",
                "Please order at least one stationery item."
            )

    def refresh_order(self):
        for entry in self.item_quantities.values():
            entry.delete(0, tk.END)

        messagebox.showinfo(
            "Refreshed",
            "Previous order has been cleared. You can place a new order!"
        )


if __name__ == "__main__":

    root = tk.Tk()

    app = StationeryOrderManagement(root)

    root.mainloop()