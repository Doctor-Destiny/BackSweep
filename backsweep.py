from customtkinter import *
import os, sys
import subprocess

set_appearance_mode("dark")

app = CTk()
app.geometry("600x400")
app.title("BackSweep")

# === Outer frame ===
main_frame = CTkFrame(master=app, fg_color="#2A2A2A")
main_frame.pack(fill="both", expand=True)

# === Left panel (tab buttons) ===
side_panel = CTkFrame(master=main_frame, width=120, fg_color="#1E1E1E")
side_panel.pack(side="left", fill="y")

# === Right panel (tab content) ===
content_frame = CTkFrame(master=main_frame, fg_color="#333333")
content_frame.pack(side="right", fill="both", expand=True)

# === Create tab pages ===
dashboard_tab = CTkFrame(master=content_frame, fg_color="#333333")
proxy_tab = CTkFrame(master=content_frame, fg_color="#333333")
repeater_tab = CTkFrame(master=content_frame, fg_color="#333333")

# === Global State ===
intercept_state = "Off"
intercept_label_text = "Turn Intercept On"
intercept_is_on = "False"

# === Intercept toggle function ===
def toggle_intercept():
    global intercept_state, intercept_label_text, intercept_is_on

    if intercept_state == "Off":
        intercept_state = "On"
        intercept_is_on = "True"
    else:
        intercept_state = "Off"
        intercept_is_on = "False"

    if intercept_label_text == "Turn Intercept Off":
        intercept_label_text = "Turn Intercept On"
    else:
        intercept_label_text = "Turn Intercept Off"

    intercept_label.configure(text=intercept_label_text)
    intercept_switch.configure(text=intercept_state)

# === Proxy Tab Content ===
intercept_label = CTkLabel(proxy_tab, text=intercept_label_text, text_color="white")
intercept_label.pack(pady=20)

intercept_switch = CTkSwitch(proxy_tab, text=intercept_state, command=toggle_intercept)
intercept_switch.pack(pady=10)

input_label = CTkLabel(proxy_tab, text="Enter Web Address:", text_color="white")
input_label.pack(pady=(20, 5))

proxy_input = CTkEntry(proxy_tab, placeholder_text="http://example.com", width=200)
proxy_input.pack(pady=5)

dropdown_label_proxy = CTkLabel(proxy_tab, text="Select Request Type:", text_color="white")
dropdown_label_proxy.pack(pady=(20, 5))

request_type_dropdown = CTkOptionMenu(proxy_tab, values=["Get", "Post"])
request_type_dropdown.pack(pady=5)
request_type_dropdown.set("Get")

console_label = CTkLabel(proxy_tab, text="Response:", text_color="white")
console_label.pack(pady=(20, 5))

console_frame = CTkFrame(proxy_tab, fg_color="#1A1A1A", border_color="#FFCC70", border_width=2)
console_frame.pack(pady=5, padx=10, fill="both", expand=False)

console_output = CTkTextbox(console_frame, width=400, height=150)
console_output.pack(padx=5, pady=5, fill="both", expand=True)
console_output.insert("end", "Waiting for response...\n")

# === Repeater Tab Content ===
dropdown_label_repeater = CTkLabel(repeater_tab, text="Select Vulnerability Type:", text_color="white")
dropdown_label_repeater.pack(pady=(20, 5))

attack_type_dropdown = CTkOptionMenu(repeater_tab, values=["NoSql Injection", "Sql Injection"])
attack_type_dropdown.pack(pady=5)
attack_type_dropdown.set("NoSql Injection")

repeater_console_label = CTkLabel(repeater_tab, text="Response:", text_color="white")
repeater_console_label.pack(pady=(20, 5))

repeater_console_frame = CTkFrame(repeater_tab, fg_color="#1A1A1A", border_color="#FFCC70", border_width=2)
repeater_console_frame.pack(pady=5, padx=10, fill="both", expand=False)

# ✅ FIX: Proper parent frame used
repeater_console_output = CTkTextbox(repeater_console_frame, width=400, height=150)
repeater_console_output.pack(padx=5, pady=5, fill="both", expand=True)
repeater_console_output.insert("end", "Waiting for response...\n")

# === Console Redirect Class ===
class ConsoleRedirect:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert("end", text)
        self.widget.see("end")

    def flush(self):
        pass

sys.stdout = ConsoleRedirect(console_output)

# === Console Redirect Class ===
class RepeaterConsoleRedirect:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert("end", text)
        self.widget.see("end")

    def flush(self):
        pass

sys.stdout = RepeaterConsoleRedirect(repeater_console_output)

# === Request Handler ===
def request():
    global last_request_url, last_request_type

    console_output.delete("1.0", "end")
    if intercept_is_on == "True":
        print("Intercept is on")
        print("Selected Request Type:", request_type_dropdown.get())
        print("Web Address:", proxy_input.get())

        url = proxy_input.get()
        req_type = request_type_dropdown.get()

        # Update dashboard info
        last_request_url = url
        last_request_type = req_type
        update_dashboard()

        try:
            if req_type == "Get":
                print("Sending GET request to", url)
                result = subprocess.run(["python", "get_request.py", url],
                                        capture_output=True, text=True, check=True)
                console_output.insert("end", result.stdout)

            elif req_type == "Post":
                print("Sending POST request to", url)
                result = subprocess.run(["python", "post_request.py", url],
                                        capture_output=True, text=True, check=True)
                console_output.insert("end", result.stdout)

        except subprocess.CalledProcessError as e:
            console_output.insert("end", f"Error:\n{e.stderr}\n")

    else:
        print("Intercept is OFF. Request not sent.")

def send_requestToRepeater():
    repeater_console_output.delete("1.0", "end")
    global intercept_is_on
    if intercept_is_on == "True":
        url = proxy_input.get()
        req_type = request_type_dropdown.get()

        try:
            if req_type == "Get":
                print("Method: GET")
                print("Url: ", url)
                result = subprocess.run(["python", "get_request.py", url],
                                        capture_output=True, text=True, check=True)
                repeater_console_output.insert("end", result.stdout)

            elif req_type == "Post":
                print("Method: POST")
                print("Url: ", url)
                result = subprocess.run(["python", "post_request.py", url],
                                        capture_output=True, text=True, check=True)
                repeater_console_output.insert("end", result.stdout)

        except subprocess.CalledProcessError as e:
            repeater_console_output.insert("end", f"Error:\n{e.stderr}\n")

def send():
    repeater_console_output.delete("1.0", "end")
    url = proxy_input.get()
    att_type = attack_type_dropdown.get()

    if att_type == "NoSql Injection":
        result = subprocess.run(["python", "nosql_inject.py", url],
                                capture_output=True, text=True, check=True)
        repeater_console_output.insert("end", result.stdout)
    elif att_type == "Sql Injection":
        result = subprocess.run(["python", "sql_inject.py", url],
                                capture_output=True, text=True, check=True)
        repeater_console_output.insert("end", result.stdout)
        
# --- New global state variables for dashboard info ---
last_request_url = "N/A"
last_request_type = "N/A"

# --- Clear existing dashboard content ---
for widget in dashboard_tab.winfo_children():
    widget.destroy()

from datetime import datetime
import threading

last_request_type = "POST"
last_request_url = "https://api.service.com/auth"

request_count = 8
success_count = 6
fail_count = 2

# Sample request history list (fill this dynamically in your app)
request_history = [
    {"method": "GET", "url": "https://example.com/login", "status": 200},
    {"method": "POST", "url": "https://api.test.com/send", "status": 403},
    {"method": "GET", "url": "https://another.io/home", "status": 200},
]

# Reset dashboard
for widget in dashboard_tab.winfo_children():
    widget.destroy()

# Welcome Header
CTkLabel(dashboard_tab, text="🔐 BackSweep Dashboard", font=CTkFont(size=22, weight="bold")).pack(pady=(20, 5))
CTkLabel(dashboard_tab, text="Welcome back! Here's your current app status:", font=CTkFont(size=14), text_color="gray").pack()

# Info Grid
info_frame = CTkFrame(dashboard_tab, fg_color="transparent")
info_frame.pack(pady=20)

intercept_status = CTkLabel(info_frame, text=f"🛡️ Intercept: {intercept_state}", font=CTkFont(size=14))
intercept_status.grid(row=0, column=0, padx=20, pady=10)

last_req_type = CTkLabel(info_frame, text=f"📤 Last Request: {last_request_type}", font=CTkFont(size=14))
last_req_type.grid(row=0, column=1, padx=20, pady=10)

last_url = CTkLabel(info_frame, text=f"🌐 Last URL:\n{last_request_url}", font=CTkFont(size=14), wraplength=300, justify="left")
last_url.grid(row=1, column=0, columnspan=2, padx=20, pady=10)

# Stats
stats_frame = CTkFrame(dashboard_tab, fg_color="#1e1e1e", corner_radius=10)
stats_frame.pack(pady=10, padx=40, fill="x")

CTkLabel(stats_frame, text="📊 Request Stats", font=CTkFont(size=16, weight="bold")).pack(pady=(10, 5))

total_requests_label = CTkLabel(stats_frame, text="Total Requests: 0", font=CTkFont(size=14))
total_requests_label.pack()

successful_requests_label = CTkLabel(stats_frame, text="Successful: 0", font=CTkFont(size=14))
successful_requests_label.pack()

failed_requests_label = CTkLabel(stats_frame, text="Failed: 0", font=CTkFont(size=14))
failed_requests_label.pack()

refresh_timer_label = CTkLabel(stats_frame, text="Last Updated: --", font=CTkFont(size=12), text_color="gray")
refresh_timer_label.pack(pady=(5, 10))

# History Box
history_frame = CTkFrame(dashboard_tab, corner_radius=10, fg_color="#1a1a1a")
history_frame.pack(pady=20, padx=40, fill="both", expand=True)

CTkLabel(history_frame, text="🕓 Recent Requests", font=CTkFont(size=16, weight="bold")).pack(pady=(10, 5))

history_box = CTkTextbox(history_frame, height=140)
history_box.pack(padx=10, pady=10, fill="both", expand=True)
history_box.configure(state="disabled")

# --- Update Function ---
def update_dashboard():
    intercept_status.configure(text=f"🛡️ Intercept: {intercept_state}")
    last_url.configure(text=f"🌐 Last URL:\n{last_request_url}")
    last_req_type.configure(text=f"📤 Last Request: {last_request_type}")
    total_requests_label.configure(text=f"Total Requests: {request_count}")
    successful_requests_label.configure(text=f"Successful: {success_count}")
    failed_requests_label.configure(text=f"Failed: {fail_count}")
    refresh_timer_label.configure(text=f"Last Updated: {datetime.now().strftime('%H:%M:%S')}")

    # Update history
    history_box.configure(state="normal")
    history_box.delete("0.0", "end")
    for r in reversed(request_history[-6:]):  # show last 6
        status_color = "green" if r["status"] == 200 else "red"
        history_box.insert("end", f'{r["method"]} - {r["url"]}\n', ("status",))
        history_box.insert("end", f'Status: {r["status"]}\n\n')
    history_box.tag_config("status", foreground="white")
    history_box.configure(state="disabled")

# --- Live Auto-Refresher ---
def auto_refresh():
    update_dashboard()
    dashboard_tab.after(5000, auto_refresh)  # refresh every 5 seconds

auto_refresh()  # Start it on load

# === Buttons ===
CTkButton(proxy_tab, text="Request", command=request).pack(pady=10)
CTkButton(proxy_tab, text="Send to Repeater", command=send_requestToRepeater).pack(pady=10)
CTkButton(repeater_tab, text="Send", command=send).pack(pady=10)

# === Tab switching ===
def show_tab(tab):
    for widget in content_frame.winfo_children():
        widget.pack_forget()
    tab.pack(fill="both", expand=True)

tab_btn_dashboard = CTkButton(side_panel, text="Dashboard", corner_radius=0,
    fg_color="#444444", hover_color="#555555", command=lambda: show_tab(dashboard_tab))
tab_btn_dashboard.pack(fill="x", pady=(10, 0), padx=10)

tab_btn_proxy = CTkButton(side_panel, text="Proxy", corner_radius=0,
    fg_color="#444444", hover_color="#555555", command=lambda: show_tab(proxy_tab))
tab_btn_proxy.pack(fill="x", pady=5, padx=10)

tab_btn_repeater = CTkButton(side_panel, text="Repeater", corner_radius=0,
    fg_color="#444444", hover_color="#555555", command=lambda: show_tab(repeater_tab))
tab_btn_repeater.pack(fill="x", pady=5, padx=10)

show_tab(dashboard_tab)
app.mainloop()
