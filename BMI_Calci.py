import tkinter as tk
from tkinter import messagebox, simpledialog
import csv
import os
import matplotlib.pyplot as plt
from datetime import datetime

DATA_FILE = 'bmi_data.csv'

def calculate_bmi(weight, height):
    return round(weight / (height ** 2), 2)

def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def save_data(name, weight, height, bmi, category):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(DATA_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, weight, height, bmi, category, date])

def show_trend(name):
    dates, bmis = [], []

    if not os.path.exists(DATA_FILE):
        messagebox.showinfo("Info", "No data found.")
        return

    with open(DATA_FILE, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == name:
                dates.append(row[5])
                bmis.append(float(row[3]))

    if not bmis:
        messagebox.showinfo("Info", "No records for user.")
        return

    plt.plot(dates, bmis, marker='o')
    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.title(f"BMI Trend for {name}")
    plt.tight_layout()
    plt.grid()
    plt.show()

def calculate():
    name = name_entry.get()
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if weight <= 0 or height <= 0:
            raise ValueError

        bmi = calculate_bmi(weight, height)
        category = classify_bmi(bmi)

        result_label.config(text=f"BMI: {bmi} ({category})")
        save_data(name, weight, height, bmi, category)

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers.")

def show_user_trend():
    name = name_entry.get()
    if name:
        show_trend(name)
    else:
        messagebox.showerror("Missing Name", "Please enter a user name.")

# GUI Setup
window = tk.Tk()
window.title("BMI Calculator")
window.geometry("350x300")
window.resizable(False, False)

tk.Label(window, text="User Name:").pack()
name_entry = tk.Entry(window)
name_entry.pack()

tk.Label(window, text="Weight (kg):").pack()
weight_entry = tk.Entry(window)
weight_entry.pack()

tk.Label(window, text="Height (m):").pack()
height_entry = tk.Entry(window)
height_entry.pack()

tk.Button(window, text="Calculate BMI", command=calculate).pack(pady=10)
result_label = tk.Label(window, text="")
result_label.pack()

tk.Button(window, text="Show Trend", command=show_user_trend).pack(pady=5)

window.mainloop()