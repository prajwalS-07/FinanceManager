import customtkinter as ctk
import mysql.connector as mys
import sys
from datetime import date
import os
from dotenv import load_dotenv

load_dotenv()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

try:
    con = mys.connect(host="localhost",
                    user="root",
                    password=os.getenv("PASSWORD_DB"),
                    database="expenseTracker")
    cur = con.cursor()
    cur.execute("create table if not exists expenses(Id int auto_increment primary key, Date timestamp default current_timestamp, Food int default 0, Travel int default 0, Others int default 0, Total int as (food+travel+others))")
    cur.execute("CREATE TABLE IF NOT EXISTS account (id INT PRIMARY KEY, balance INT)")
    cur.execute("INSERT IGNORE INTO account (id, balance) VALUES (1, 7433)")
    con.commit()

except Exception as e:
    print(f"Error: {e}. Check SQL")
    sys.exit()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x350")
        self.title("Expense Tracker")
        
        cur.execute("SELECT balance FROM account WHERE id = 1")
        result = cur.fetchone()
        self.total_balance = result[0] if result else 0

        self.setup_ui()
        

    def setup_ui(self):
        self.main_label = ctk.CTkLabel(self, text="MAIN MENU", font=("Arial", 20, "bold"))
        self.main_label.pack(pady=(30, 10))

        self.addExpenseBtn = ctk.CTkButton(self, text="Add New Expense", 
                                           command=self.add_expense,
                                           height=45, width=200,
                                           corner_radius=12,
                                           font=("Arial", 14, "bold"),
                                           border_width=2,
                                           border_color="#1f538d",
                                           fg_color="#243b55")
        self.addExpenseBtn.pack(pady=15)

        self.viewExpenseBtn = ctk.CTkButton(self, text="View Records", 
                                            command=self.view_expenses,
                                            height=45, width=200,
                                            corner_radius=12,
                                            font=("Arial", 14, "bold"),
                                            border_width=2,
                                            border_color="#1f538d",
                                            fg_color="#243b55")
        self.viewExpenseBtn.pack(pady=15)

        self.currentBal = ctk.CTkLabel(self, text=f"Current Balance: Rs. {self.total_balance}", font=("Arial", 14, "bold"))
        self.currentBal.pack(pady=15)

    def updateBalance(self):
        self.currentBal.configure(text=f"Current Balance: Rs. {self.total_balance}")


    def add_expense(self):
        self.addExpenseWindow = ctk.CTkToplevel(self)
        self.addExpenseWindow.title("Add Entry")
        self.addExpenseWindow.geometry("350x500")
        self.addExpenseWindow.attributes("-topmost", True)

        ctk.CTkLabel(self.addExpenseWindow, text="EXPENSE DETAILS", font=("Arial", 16, "bold")).pack(pady=20)

        
        today = date.today().strftime('%Y-%m-%d')
        self.manual_date = ctk.CTkEntry(self.addExpenseWindow, width=250, height=35, corner_radius=10, border_color="#3b8ed0")
        self.manual_date.insert(0, today) 
        self.manual_date.pack(pady=5)
        
        ctk.CTkLabel(self.addExpenseWindow, text="YYYY-MM-DD", font=("Arial", 10, "italic")).pack(pady=(0,10))

        self.food = ctk.CTkEntry(self.addExpenseWindow, placeholder_text="Food Amount", width=220, height=35, corner_radius=10)
        self.food.pack(pady=10)

        self.travel = ctk.CTkEntry(self.addExpenseWindow, placeholder_text="Travel Amount", width=220, height=35, corner_radius=10)
        self.travel.pack(pady=10)

        self.others = ctk.CTkEntry(self.addExpenseWindow, placeholder_text="Others Amount", width=220, height=35, corner_radius=10)
        self.others.pack(pady=10)

        self.saveBtn = ctk.CTkButton(self.addExpenseWindow, text="Save Entry", 
                                     command=self.save, 
                                     height=40, width=150, 
                                     corner_radius=12, font=("Arial", 13, "bold"))
        self.saveBtn.pack(pady=20)

        
        self.clearBtn = ctk.CTkButton(self.addExpenseWindow, text="Clear Form", 
                                      command=self.clear_form, 
                                      height=30, width=100, 
                                      fg_color="transparent", border_width=1)
        self.clearBtn.pack(pady=5)
        self.addExpenseWindow.bind("<Return>",self.save)

    def clear_form(self):
        self.food.delete(0, 'end')
        self.travel.delete(0, 'end')
        self.others.delete(0, 'end')
        self.manual_date.delete(0, 'end')
        self.manual_date.insert(0, date.today().strftime('%Y-%m-%d'))

    def save(self, event=None):
        try:
            f = int(self.food.get() or 0)
            t = int(self.travel.get() or 0)
            o = int(self.others.get() or 0)
            user_date = self.manual_date.get().strip()

            
            query = "INSERT INTO expenses (Date, Food, Travel, Others) VALUES (%s, %s, %s, %s)"
            values = (user_date, f, t, o)

            cur.execute(query, values)
            con.commit()

            self.total_balance -= (f+t+o)

            cur.execute("UPDATE account SET balance = %s WHERE id = 1", (self.total_balance,))
            con.commit()

            self.updateBalance()
            
            self.saveBtn.configure(text="Data Saved!", fg_color="green")
            
            
            self.food.delete(0, 'end')
            self.travel.delete(0, 'end')
            self.others.delete(0, 'end')

            self.after(1500, lambda: self.saveBtn.configure(text="Save Entry", fg_color="#1f6aa5"))

        except Exception as e:
            print(f"Error: {e}. Check date format (YYYY-MM-DD) and ensure amounts are numbers.")

    def view_expenses(self):
        self.viewExpenseWindow = ctk.CTkToplevel(self)
        self.viewExpenseWindow.title("View Records")
        self.viewExpenseWindow.geometry("350x400")
        self.viewExpenseWindow.attributes("-topmost", True)

        ctk.CTkLabel(self.viewExpenseWindow, text="FILTER", font=("Arial", 16, "bold")).pack(pady=20)

        self.entryByDate = ctk.CTkButton(self.viewExpenseWindow, text="Search by Date", 
                                         command=self.byDate,
                                         width=180, height=40, corner_radius=12,
                                         font=("Arial", 13, "bold"),
                                         border_width=2,
                                         border_color="#1f538d",
                                         fg_color="#243b55")
        self.entryByDate.pack(pady=10)

        self.entryByMonth = ctk.CTkButton(self.viewExpenseWindow, text="Search by Month",
                                          command=self.byMonth,
                                          width=180, height=40, corner_radius=12,
                                          font=("Arial", 13, "bold"),
                                          border_width=2,
                                          border_color="#1f538d",
                                          fg_color="#243b55")
        self.entryByMonth.pack(pady=10)

    def byDate(self):
        self.viewExpenseWindow.destroy()
        self.byDateWindow = ctk.CTkToplevel(self)
        self.byDateWindow.title("Search by Date")
        self.byDateWindow.geometry("500x500")
        self.byDateWindow.attributes("-topmost", True)

        self.enterDate = ctk.CTkEntry(self.byDateWindow, placeholder_text="YYYY-MM-DD", font=("Arial", 12, "bold"), width=220, corner_radius=10)
        self.enterDate.pack(pady=20)

        findEntry1 = ctk.CTkButton(self.byDateWindow, text="Get Entries", command=self.find1, corner_radius=10, font=("Arial", 12, "bold"))
        findEntry1.pack(pady=5)

        self.byDateWindow.bind("<Return>",self.find1)

    def find1(self, event=None):
        if hasattr(self, 'scroll_frame'):
            self.scroll_frame.destroy()

        date_val = self.enterDate.get()
        query = "SELECT Date, Food, Travel, Others, Total FROM expenses WHERE DATE(Date) = %s"
        cur.execute(query, (date_val,))
        results = cur.fetchall()

        self.scroll_frame = ctk.CTkScrollableFrame(self.byDateWindow, width=450, height=250, corner_radius=12, border_width=2, border_color="#1f538d")
        self.scroll_frame.pack(pady=20, padx=10)

        if not results:
            ctk.CTkLabel(self.scroll_frame, text="No data found.", font=("Arial", 12, "italic")).pack(pady=10)
        else:
            header = ctk.CTkLabel(self.scroll_frame, text="Food | Travel | Others | Total", font=("Arial", 12, "bold"), text_color="#3b8ed0")
            header.pack(pady=5)

            for row in results:
                display_text = f"Rs. {row[1]} | Rs. {row[2]} | Rs. {row[3]} | Sum: Rs. {row[4]}"
                result_label = ctk.CTkLabel(self.scroll_frame, text=display_text, font=("Courier", 12))
                result_label.pack(pady=2, anchor="w")

    def byMonth(self):
        self.viewExpenseWindow.destroy()
        self.byMonthWindow = ctk.CTkToplevel(self)
        self.byMonthWindow.title("Search by Month")
        self.byMonthWindow.geometry("350x500")
        self.byMonthWindow.attributes("-topmost", True)

        ctk.CTkLabel(self.byMonthWindow, text="MONTHLY SEARCH", font=("Arial", 15, "bold")).pack(pady=15)
        
        self.monthEntry = ctk.CTkEntry(self.byMonthWindow, placeholder_text="Month (1-12)", font=("Arial", 12, "bold"), width=180, corner_radius=10)
        self.monthEntry.pack(pady=5)

        self.yearEntry = ctk.CTkEntry(self.byMonthWindow, placeholder_text="Year (YYYY)", font=("Arial", 12, "bold"), width=180, corner_radius=10)
        self.yearEntry.pack(pady=5)

        findBtn = ctk.CTkButton(self.byMonthWindow, text="Calculate Totals", command=self.findMonth, corner_radius=10, font=("Arial", 12, "bold"))
        findBtn.pack(pady=15)

        self.byMonthWindow.bind("<Return>",self.findMonth)

    def findMonth(self, event=None):
        if hasattr(self, 'month_scroll'):
            self.month_scroll.destroy()

        m = self.monthEntry.get()
        y = self.yearEntry.get()
        query = "SELECT SUM(Food), SUM(Travel), SUM(Others), SUM(Total) FROM expenses WHERE MONTH(Date) = %s AND YEAR(Date) = %s"
        
        try:
            cur.execute(query, (m, y))
            result = cur.fetchone() 

            self.month_scroll = ctk.CTkScrollableFrame(self.byMonthWindow, width=300, height=220, corner_radius=12, border_width=2, border_color="#1f538d")
            self.month_scroll.pack(pady=10)

            if result[0] is None: 
                ctk.CTkLabel(self.month_scroll, text="No records found.").pack(pady=10)
            else:
                ctk.CTkLabel(self.month_scroll, text=f"SUMMARY: {m}/{y}", font=("Arial", 14, "bold"), text_color="#3b8ed0").pack(pady=10)
                
                stats = [
                    f"Food:   Rs. {result[0]}",
                    f"Travel: Rs. {result[1]}",
                    f"Others: Rs. {result[2]}",
                    "--------------------",
                    f"TOTAL:  Rs. {result[3]}"
                ]

                for item in stats:
                    lbl = ctk.CTkLabel(self.month_scroll, text=item, font=("Courier", 14, "bold"))
                    lbl.pack(pady=3, anchor="w")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()