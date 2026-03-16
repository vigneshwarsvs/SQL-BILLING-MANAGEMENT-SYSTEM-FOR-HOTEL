import os
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from sqlalchemy import (
    create_engine, Column, Integer, String, Numeric, DateTime, ForeignKey, func
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# -----------------------
# Database configuration
# -----------------------
DB_CONFIG = {
    "USERNAME": "Heisenberg",  # change if needed
    "PASSWORD": "saymyname",  # change if needed
    "HOST": "localhost",
    "DATABASE": "pythonclassoops",
    "ECHO": True,
}

DATABASE_URL = f"mysql+pymysql://{DB_CONFIG['USERNAME']}:{DB_CONFIG['PASSWORD']}@{DB_CONFIG['HOST']}/{DB_CONFIG['DATABASE']}"

engine = create_engine(DATABASE_URL, echo=DB_CONFIG["ECHO"], pool_pre_ping=True)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# -----------------------
# Models
# -----------------------
class MenuItem(Base):
    __tablename__ = "menu_items"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    price = Column(Numeric(10, 2), nullable=False)


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now())
    subtotal = Column(Numeric(12, 2))
    tax_pct = Column(Numeric(5, 2))
    total = Column(Numeric(12, 2))

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    name = Column(String(100))
    unit_price = Column(Numeric(10, 2))
    quantity = Column(Integer)
    line_total = Column(Numeric(12, 2))

    order = relationship("Order", back_populates="items")


Base.metadata.create_all(engine)

def money(v):
    return Decimal(str(v)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def seed_menu():
    if session.query(MenuItem).count() == 0:
        sample = [
            ("Burger", 120),
            ("Pizza", 350),
            ("Fries", 90),
            ("Coke", 50),
        ]
        for name, price in sample:
            session.add(MenuItem(name=name, price=money(price)))
        session.commit()


seed_menu()

class BillingApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Restaurant Billing System")
        self.geometry("1000x600")
        self.cart = {}
        self.tax_pct = Decimal("5.00")

        self.current_subtotal = Decimal("0.00")
        self.current_tax = Decimal("0.00")
        self.current_total = Decimal("0.00")
        self.create_widgets()
        self.load_menu()

    def create_widgets(self):   
        # LEFT - MENU
        left = ttk.Frame(self, padding=10)
        left.place(x=10, y=10, width=450, height=580)

        ttk.Label(left, text="Menu", font=("Arial", 14)).pack(anchor="w")
        self.menu_tree = ttk.Treeview(left, columns=("name", "price"), show="headings")
        self.menu_tree.heading("name", text="Item")
        self.menu_tree.heading("price", text="Price")
        self.menu_tree.column("name", width=280)
        self.menu_tree.column("price", width=120, anchor="e")
        self.menu_tree.pack(fill="both", expand=True, pady=10)

        ttk.Button(left, text="Add Selected",command=self.add_selected).pack(pady=3)
        ttk.Button(left, text="Add New Menu Item",command=self.add_menu_item).pack(pady=3)

        right = ttk.Frame(self, padding=10)
        right.place(x=480, y=10, width=1000, height=580)

        ttk.Label(right, text="Cart", font=("Arial", 14)).pack(anchor="w")

        self.cart_tree = ttk.Treeview(right, columns=("name", "qty", "price", "total"), show="headings")
        self.cart_tree.heading("name", text="Item")
        self.cart_tree.heading("qty", text="Qty")
        self.cart_tree.heading("price", text="Unit")
        self.cart_tree.heading("total", text="Total")
        self.cart_tree.pack(fill="both", expand=True, pady=10)

        ttk.Button(right, text="Remove Selected",command=self.remove_selected).pack()

        self.total_var = tk.StringVar(value="0.00")

        ttk.Label(right, text="Grand Total:", font=("Arial", 12)).pack(anchor="w", pady=5)
        ttk.Label(right, textvariable=self.total_var, font=("Arial", 14, "bold")).pack(anchor="w")

        ttk.Button(right, text="Generate Bill",command=self.generate_bill).pack(pady=5)
        ttk.Button(right, text="Save Bill",command=self.save_bill).pack(pady=5)

    def load_menu(self):
        for row in self.menu_tree.get_children():
            self.menu_tree.delete(row)

        items = session.query(MenuItem).order_by(MenuItem.name).all()
        for item in items:
            self.menu_tree.insert("", "end", iid=str(item.id),
                                  values=(item.name, money(item.price)))

    def add_menu_item(self):
        name = simpledialog.askstring("Item Name", "Enter item name:")
        price = simpledialog.askfloat("Price", "Enter price:")
        session.add(MenuItem(name=name, price=money(price)))
        session.commit()
        self.load_menu()
        messagebox.showinfo("Success", "Menu item added.")

    def add_selected(self):
        sel = self.menu_tree.selection()
        if not sel:
            return
        item_id = int(sel[0])
        item = session.get(MenuItem, item_id)

        qty = simpledialog.askinteger("Quantity", "Enter quantity:", minvalue=1)
        if not qty:
            return

        if item_id in self.cart:
            self.cart[item_id]["qty"] += qty
        else:
            self.cart[item_id] = {"item": item, "qty": qty}

        self.refresh_cart()

    def remove_selected(self):
        sel = self.cart_tree.selection()
        if sel:
            del self.cart[int(sel[0])]
            self.refresh_cart()

    def refresh_cart(self):
        for row in self.cart_tree.get_children():
            self.cart_tree.delete(row)

        subtotal = Decimal("0.00")

        for item_id, data in self.cart.items():
            item = data["item"]
            qty = data["qty"]
            line = money(item.price * qty)
            subtotal += line

            self.cart_tree.insert("", "end", iid=str(item_id),
                                  values=(item.name, qty, money(item.price), line))

        tax = money(subtotal * (self.tax_pct / 100))
        grand_total = money(subtotal + tax)

        self.current_subtotal = subtotal
        self.current_tax = tax
        self.current_total = grand_total

        self.total_var.set(str(grand_total))

    def generate_bill(self):
        if not self.cart:
            messagebox.showwarning("Empty", "Cart is empty")
            return

        bill_text = self.create_bill_text()

        win = tk.Toplevel(self)
        win.title("Bill")

        txt = tk.Text(win, width=70, height=25)
        txt.pack()
        txt.insert("1.0", bill_text)
        txt.config(state="disabled")

    def create_bill_text(self):
        lines = []
        lines.append("===== RESTAURANT BILL =====")
        lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("-" * 40)

        for data in self.cart.values():
            item = data["item"]
            qty = data["qty"]
            line = money(item.price * qty)
            lines.append(f"{item.name} x{qty} = {line}")

        lines.append("-" * 40)
        lines.append(f"Subtotal: {self.current_subtotal}")
        lines.append(f"Tax (5%): {self.current_tax}")
        lines.append(f"TOTAL: {self.current_total}")
        lines.append("=" * 40)

        return "\n".join(lines)

    def save_bill(self):
        if not self.cart:
            messagebox.showwarning("Empty", "Cart is empty")
            return

        order = Order(
            created_at=datetime.now(),
            subtotal=self.current_subtotal,
            tax_pct=self.tax_pct,
            total=self.current_total
        )

        for data in self.cart.values():
            item = data["item"]
            qty = data["qty"]
            order.items.append(OrderItem(
                name=item.name,
                unit_price=item.price,
                quantity=qty,
                line_total=money(item.price * qty)
            ))

        session.add(order)
        session.commit()

        bill_text = self.create_bill_text()

        filename = f"bill_{order.id}.txt"
        filepath = os.path.join(os.getcwd(), filename)

        with open(filepath, "w") as f:
            f.write(bill_text)

        messagebox.showinfo("Saved", f"Bill saved successfully!\n{filepath}")

        self.cart.clear()
        self.refresh_cart()

if __name__ == "__main__":
    app = BillingApp()
    app.mainloop()