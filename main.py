import requests
import concurrent.futures
import tkinter as tk
from tkinter import filedialog
import tkinter.font as tkfont
import sys

# Color constants
PRIMARY_COLOR = "#6495ED"  # Cornflower Blue
SECONDARY_COLOR = "#010305"  # #030a14.#061124
BUTTON_COLOR = "#bf8c2e"  # Orange
HAMBURGER_COLOR = "#FFD700"  # Yellow

def send_sms(phone_number, message):
    try:
        headers = {'Authorization': f"Bearer {api_token.get()}", 'Content-Type': 'application/json'}
        data = {
            'name': api_name.get(),
            'service_plan_id': api_service_plan_id.get(),
            'to': phone_number,
            'message': message
        }
        response = requests.post(api_url.get(), headers=headers, json=data)
        response.raise_for_status()
        return f"SMS sent to {phone_number}\n"
    except requests.exceptions.HTTPError as errh:
        return f"HTTP Error: {errh}\n"
    except requests.exceptions.ConnectionError as errc:
        return f"Error Connecting: {errc}\n"
    except requests.exceptions.Timeout as errt:
        return f"Timeout Error: {errt}\n"
    except requests.exceptions.RequestException as err:
        return f"Something went wrong: {err}\n"

def send_sms_to_numbers():
    message = sms_text.get('1.0', tk.END).strip()
    phone_numbers = phone_numbers_text.get('1.0', tk.END).strip().split('\n')

    error_messages = []

    if not api_name.get():
        error_messages.append("Error: API Name is empty")

    if not api_service_plan_id.get():
        error_messages.append("Error: Service Plan ID is empty")

    if not api_token.get():
        error_messages.append("Error: API Token is empty")

    if not api_url.get():
        error_messages.append("Error: API URL is empty")

    if not message:
        error_messages.append("Error: SMS body is empty")

    if not phone_numbers:
        error_messages.append("Error: Phone numbers are empty")

    if error_messages:
        status_text.insert(tk.END, "\n".join(error_messages))
        return

    invalid_numbers = []
    for number in phone_numbers:
        number = number.strip()
        if not number.isdigit() or len(number) != 10:
            invalid_numbers.append(number)

    if invalid_numbers:
        error_message = "Error: Invalid phone number(s):\n"
        error_message += "\n".join(invalid_numbers)
        status_text.insert(tk.END, error_message)
        return

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for number in phone_numbers:
            futures.append(executor.submit(send_sms, number, message))

        for future in concurrent.futures.as_completed(futures):
            status_message = future.result()
            status_text.insert(tk.END, status_message)
            window.update()

def browse_file():
    filename = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
    if filename:
        with open(filename, 'r') as file:
            phone_numbers_text.delete('1.0', tk.END)
            phone_numbers_text.insert(tk.END, file.read())

def exit_app():
    window.destroy()
    sys.exit()

def toggle_menu():
    if menu_frame.winfo_ismapped():
        menu_frame.grid_remove()
    else:
        menu_frame.grid(row=0, column=0, padx=10, pady=5, sticky="w")


window = tk.Tk()
window.title("SMS Sender")
window.geometry("550x690")
window.resizable(False, False)
window.configure(bg=SECONDARY_COLOR)


header_frame = tk.Frame(window, bg=SECONDARY_COLOR)
header_frame.pack(pady=20)


hamburger_icon = tk.Label(header_frame, text="≡", font=("Arial", 20), bg=SECONDARY_COLOR, fg="#e3ca46")
hamburger_icon.grid(row=0, column=0, padx=10, pady=5, sticky="w")

menu_frame = tk.Frame(header_frame, bg=SECONDARY_COLOR)

hamburger_icon.bind("<Button-1>", lambda event: toggle_menu())


about_label = tk.Label(menu_frame, text="About", bg=SECONDARY_COLOR, fg="#edeef0")
about_label.pack(anchor="w")

contact_label = tk.Label(menu_frame, text="Contact", bg=SECONDARY_COLOR, fg="#edeef0")
contact_label.pack(anchor="w")

exit_label = tk.Label(menu_frame, text="Exit", bg=SECONDARY_COLOR, fg="#edeef0")
exit_label.pack(anchor="w")


menu_frame.grid_remove()

banner_font = tkfont.Font(family="Bahnschrift SemiBold", size=25)
banner_label = tk.Label(header_frame, text="Sinch Bulk SMS", font=banner_font, bg=SECONDARY_COLOR, fg="#edeef0")
banner_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")


separator = tk.Frame(window, height=4, bg="#060f1f")
separator.pack(fill=tk.X)


api_frame = tk.Frame(window, bg=SECONDARY_COLOR)
api_frame.pack(pady=20)

phone_frame = tk.Frame(window, bg=SECONDARY_COLOR)
phone_frame.pack(pady=10)

sms_frame = tk.Frame(window, bg=SECONDARY_COLOR)
sms_frame.pack(pady=10)

status_frame = tk.Frame(window, bg=SECONDARY_COLOR)
status_frame.pack(pady=10)


api_name = tk.StringVar()
api_name_label = tk.Label(api_frame, text="Name:", bg=SECONDARY_COLOR, fg="#edeef0")
api_name_label.grid(row=0, column=0, padx=10, pady=5)
api_name_entry = tk.Entry(api_frame, textvariable=api_name, width=40, bg="#04080d", fg="#edeef0", insertbackground="white")
api_name_entry.grid(row=0, column=1, padx=10, pady=5)

api_service_plan_id = tk.StringVar()
api_service_plan_id_label = tk.Label(api_frame, text="Service Plan ID:", bg=SECONDARY_COLOR, fg="#edeef0")
api_service_plan_id_label.grid(row=1, column=0, padx=10, pady=5)
api_service_plan_id_entry = tk.Entry(api_frame, textvariable=api_service_plan_id, width=40, bg="#04080d", fg="#edeef0", insertbackground="white")
api_service_plan_id_entry.grid(row=1, column=1, padx=10, pady=5)

api_token = tk.StringVar()
api_token_label = tk.Label(api_frame, text="API Token:", bg=SECONDARY_COLOR, fg="#edeef0")
api_token_label.grid(row=2, column=0, padx=10, pady=5)
api_token_entry = tk.Entry(api_frame, textvariable=api_token, width=40, bg="#04080d", fg="#edeef0", insertbackground="white")
api_token_entry.grid(row=2, column=1, padx=10, pady=5)

api_url = tk.StringVar()
api_url_label = tk.Label(api_frame, text="API URL:", bg=SECONDARY_COLOR, fg="#edeef0")
api_url_label.grid(row=3, column=0, padx=10, pady=5)
api_url_entry = tk.Entry(api_frame, textvariable=api_url, width=40, bg="#04080d", fg="#edeef0", insertbackground="white")
api_url_entry.grid(row=3, column=1, padx=10, pady=5)


phone_numbers_label = tk.Label(phone_frame, text="Phone Numbers:", bg=SECONDARY_COLOR, fg="#edeef0")
phone_numbers_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

phone_numbers_text = tk.Text(phone_frame, height=5, width=40, bg="#04080d", fg="#edeef0", insertbackground="white")
phone_numbers_text.grid(row=0, column=1, padx=10, pady=5)

browse_button = tk.Button(phone_frame, text="Browse", command=browse_file, bg=BUTTON_COLOR, fg=SECONDARY_COLOR)
browse_button.grid(row=0, column=2, padx=10, pady=5)

sms_label = tk.Label(sms_frame, text="    Message Body:   ", bg=SECONDARY_COLOR, fg="#edeef0")
sms_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

sms_text = tk.Text(sms_frame, height=10, width=40, bg="#04080d", fg="#edeef0", insertbackground="white")
sms_text.grid(row=0, column=1, padx=10, pady=5)

send_button = tk.Button(sms_frame, text="Send SMS", command=send_sms_to_numbers, bg=BUTTON_COLOR, fg=SECONDARY_COLOR)
send_button.grid(row=0, column=2, padx=10, pady=5)

status_label = tk.Label(status_frame, text="Status:", bg=SECONDARY_COLOR, fg="#edeef0")
status_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

status_text = tk.Text(status_frame, height=5, width=41, bg="#04080d", fg="#edeef0", insertbackground="white")
status_text.grid(row=0, column=1, padx=10, pady=5)


separator = tk.Frame(window, height=4, bg="#060f1f")
separator.pack(fill=tk.X)


browse_button.configure(activebackground=BUTTON_COLOR)
send_button.configure(activebackground=BUTTON_COLOR)


def about():
    status_text.delete("1.0", tk.END)
    status_text.insert(tk.END, "This application allows you to send bulk SMS messages using the Sinch SMS API.\nIf you have eny queries contact me.\nApp Version 1.00")
    toggle_menu()

def contact():
    status_text.delete("1.0", tk.END)
    status_text.insert(tk.END, "Github: https://github.com/VijayVairagade\nEmail: vijayvairagade22@gmail.com")
    toggle_menu()



about_label.bind("<Button-1>", lambda event: about())
contact_label.bind("<Button-1>", lambda event: contact())
exit_label.bind("<Button-1>", lambda event: exit_app())

menu_frame.grid_remove()

window.mainloop()

