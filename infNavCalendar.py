import calendar
import tkinter as tk

def show_calendar():
    year = int(year_entry.get())
    month = int(month_entry.get())
    
    cal_text.config(state=tk.NORMAL)
    cal_text.delete("1.0", tk.END)
    
    cal = calendar.month(year, month)
    cal_text.insert(tk.END, cal)
    cal_text.config(state=tk.DISABLED)

def next_month():
    current_year = int(year_entry.get())
    current_month = int(month_entry.get())
    
    if current_month == 12:
        current_year += 1
        current_month = 1
    else:
        current_month += 1
    
    year_entry.delete(0, tk.END)
    year_entry.insert(0, str(current_year))
    month_entry.delete(0, tk.END)
    month_entry.insert(0, str(current_month))
    show_calendar()

# Create the main window
window = tk.Tk()
window.title("Infinite Navigable Calendar")

# Create input fields and labels
year_label = tk.Label(window, text="Year (YYYY):")
year_label.pack()
year_entry = tk.Entry(window)
year_entry.pack()
year_entry.insert(0, "2023")  # Default year

month_label = tk.Label(window, text="Month (1-12):")
month_label.pack()
month_entry = tk.Entry(window)
month_entry.pack()
month_entry.insert(0, "9")  # Default month

show_button = tk.Button(window, text="Show Calendar", command=show_calendar)
show_button.pack()

next_button = tk.Button(window, text="Next Month", command=next_month)
next_button.pack()

# Create text widget to display the calendar
cal_text = tk.Text(window, height=10, width=30)
cal_text.pack()
cal_text.config(state=tk.DISABLED)

# Show the initial calendar
show_calendar()

window.mainloop()
