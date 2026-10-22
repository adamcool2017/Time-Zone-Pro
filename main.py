
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from zoneinfo import ZoneInfo, available_timezones

# ==========================================
# TIMEZONE PRO
# A beginner-friendly world clock
# ==========================================

APP_NAME = "TimeZone Pro"
BG = "#101522"
PANEL = "#192235"
CARD = "#222e45"
ACCENT = "#63a4ff"
TEXT = "#f1f5ff"
MUTED = "#9eacc5"
GREEN = "#65e6b2"

DEFAULT_CITIES = [
    ("Manama", "Asia/Bahrain"),
    ("London", "Europe/London"),
    ("New York", "America/New_York"),
    ("Tokyo", "Asia/Tokyo"),
    ("Edinburgh", "Europe/London"),
]

root = tk.Tk()
root.title(APP_NAME)
root.geometry("900x700")
root.minsize(720, 600)
root.configure(bg=BG)

cities = DEFAULT_CITIES.copy()
clock_labels = []

style = ttk.Style()
style.theme_use("clam")
style.configure(
    "TCombobox",
    fieldbackground=CARD,
    background=CARD,
    foreground=TEXT,
    arrowcolor=TEXT,
    padding=7
)


def make_label(parent, text, size=11, color=TEXT, bold=False):
    return tk.Label(
        parent,
        text=text,
        font=("Segoe UI", size, "bold" if bold else "normal"),
        bg=parent.cget("bg"),
        fg=color
    )


def make_button(parent, text, command, color=ACCENT):
    return tk.Button(
        parent,
        text=text,
        command=command,
        font=("Segoe UI", 10, "bold"),
        bg=color,
        fg=BG,
        activebackground=GREEN,
        activeforeground=BG,
        relief="flat",
        bd=0,
        padx=12,
        pady=8,
        cursor="hand2"
    )


# ---------- HEADER ----------

header = tk.Frame(root, bg=BG)
header.pack(fill="x", padx=28, pady=(22, 8))

make_label(header, "TIMEZONE PRO", 23, ACCENT, True).pack(anchor="w")
make_label(
    header,
    "YOUR WORLD, ONE CLOCK AT A TIME",
    9, MUTED, True
).pack(anchor="w", pady=(2, 0))

status_label = make_label(header, "Starting clocks...", 10, GREEN)
status_label.pack(anchor="w", pady=(8, 0))


# ---------- WORLD CLOCKS ----------

section = tk.Frame(root, bg=BG)
section.pack(fill="x", padx=28, pady=(12, 5))

make_label(section, "World clocks", 16, TEXT, True).pack(side="left")

clock_area = tk.Frame(root, bg=BG)
clock_area.pack(fill="x", padx=28)

def refresh_clocks():
    """Update every displayed clock using its own time zone."""
    for city, zone, time_label, date_label in clock_labels:
        try:
            now = datetime.now(ZoneInfo(zone))
            time_label.config(text=now.strftime("%H:%M:%S"))
            date_label.config(text=now.strftime("%A, %d %B %Y"))
        except Exception:
            time_label.config(text="Unavailable")
            date_label.config(text=zone)

    status_label.config(
        text=f"LIVE  •  {len(cities)} CITIES  •  LOCAL CLOCKS"
    )
    root.after(1000, refresh_clocks)


def redraw_clocks():
    """Rebuild the clock cards after adding or removing a city."""
    global clock_labels
    clock_labels = []

    for widget in clock_area.winfo_children():
        widget.destroy()

    for index, (city, zone) in enumerate(cities):
        card = tk.Frame(
            clock_area,
            bg=CARD,
            padx=16,
            pady=12,
            highlightbackground="#33415d",
            highlightthickness=1
        )

        card.grid(
            row=index // 3,
            column=index % 3,
            sticky="nsew",
            padx=5,
            pady=5
        )

        city_label = tk.Label(
            card, text=city.upper(),
            font=("Segoe UI", 11, "bold"),
            bg=CARD, fg=ACCENT
        )
        city_label.pack(anchor="w")

        zone_label = tk.Label(
            card, text=zone,
            font=("Segoe UI", 8),
            bg=CARD, fg=MUTED
        )
        zone_label.pack(anchor="w", pady=(2, 5))

        time_label = tk.Label(
            card, text="--:--:--",
            font=("Consolas", 23, "bold"),
            bg=CARD, fg=TEXT
        )
        time_label.pack(anchor="w")

        date_label = tk.Label(
            card, text="Loading...",
            font=("Segoe UI", 9),
            bg=CARD, fg=GREEN
        )
        date_label.pack(anchor="w", pady=(4, 0))

        clock_labels.append((city, zone, time_label, date_label))

    for column in range(3):
        clock_area.grid_columnconfigure(column, weight=1)

    refresh_clocks()


# ---------- ADD / REMOVE CITIES ----------

city_panel = tk.Frame(root, bg=PANEL, padx=14, pady=12)
city_panel.pack(fill="x", padx=28, pady=12)

make_label(city_panel, "Manage cities", 12, TEXT, True).grid(
    row=0, column=0, columnspan=3, sticky="w", pady=(0, 8)
)

zone_names = sorted(available_timezones())

city_var = tk.StringVar()
zone_var = tk.StringVar(value="Asia/Bahrain")

city_entry = tk.Entry(
    city_panel,
    textvariable=city_var,
    font=("Segoe UI", 10),
    bg=CARD, fg=TEXT,
    insertbackground=TEXT,
    relief="flat",
    width=17
)
city_entry.grid(row=1, column=0, padx=(0, 8), ipady=7)

zone_box = ttk.Combobox(
    city_panel,
    textvariable=zone_var,
    values=zone_names,
    state="readonly",
    width=30
)
zone_box.grid(row=1, column=1, padx=(0, 8))

# Search for a time zone by city, country, or time-zone name.
zone_search_var = tk.StringVar()

zone_search_entry = tk.Entry(
    city_panel,
    textvariable=zone_search_var,
    font=("Segoe UI", 10),
    bg=CARD, fg=TEXT,
    insertbackground=TEXT,
    relief="flat",
    width=25
)
zone_search_entry.grid(row=2, column=0, sticky="ew", padx=(0, 8), ipady=7)

# Common country and city names that help users find their time zones.
search_aliases = {
    "bahrain": "Asia/Bahrain",
    "manama": "Asia/Bahrain",
    "japan": "Asia/Tokyo",
    "tokyo": "Asia/Tokyo",
    "united kingdom": "Europe/London",
    "uk": "Europe/London",
    "britain": "Europe/London",
    "london": "Europe/London",
    "edinburgh": "Europe/London",
    "united states": "America/New_York",
    "usa": "America/New_York",
    "new york": "America/New_York",
    "france": "Europe/Paris",
    "paris": "Europe/Paris",
    "india": "Asia/Kolkata",
    "china": "Asia/Shanghai",
    "uae": "Asia/Dubai",
    "united arab emirates": "Asia/Dubai",
    "dubai": "Asia/Dubai",
    "singapore": "Asia/Singapore",
    "australia": "Australia/Sydney",
    "sydney": "Australia/Sydney",
    "germany": "Europe/Berlin",
    "berlin": "Europe/Berlin",
    "canada": "America/Toronto",
    "toronto": "America/Toronto",
    "south korea": "Asia/Seoul",
    "korea": "Asia/Seoul",
    "seoul": "Asia/Seoul",
    "new zealand": "Pacific/Auckland",
    "auckland": "Pacific/Auckland",
}


def search_time_zones():
    query = zone_search_var.get().strip().casefold()

    if not query:
        zone_box["values"] = zone_names
        messagebox.showinfo(
            "Search time zones",
            "Type a city, country, or time-zone name first."
        )
        return

    matching_zones = [
        zone for zone in zone_names
        if query in zone.casefold()
    ]

    # Add a matching time zone for common country/city searches.
    for alias, zone in search_aliases.items():
        if query in alias and zone in zone_names and zone not in matching_zones:
            matching_zones.append(zone)

    zone_box["values"] = matching_zones

    if len(matching_zones) == 1:
        zone_var.set(matching_zones[0])
        messagebox.showinfo(
            "Search complete",
            f"Found: {matching_zones[0]}"
        )
    elif matching_zones:
        zone_box.current(0)
        messagebox.showinfo(
            "Search complete",
            f"Found {len(matching_zones)} matching time zones. Choose one from the list."
        )
        zone_box.event_generate("<<ComboboxSelected>>")
    else:
        zone_box["values"] = zone_names
        messagebox.showinfo(
            "No results",
            "No matching time zones found. Try a city, country, or a name like Asia/Tokyo."
        )


def reset_time_zone_search():
    zone_search_var.set("")
    zone_box["values"] = zone_names


make_button(city_panel, "Search", search_time_zones).grid(
    row=2, column=1, sticky="w", padx=(0, 8)
)

make_button(city_panel, "Reset search", reset_time_zone_search, MUTED).grid(
    row=2, column=2, sticky="w"
)


def add_city():
    city = city_var.get().strip()
    zone = zone_var.get().strip()

    if not city:
        messagebox.showwarning(
            "Missing city", "Please enter a city name."
        )
        return

    if not zone:
        messagebox.showwarning(
            "Missing time zone", "Please choose a time zone."
        )
        return

    if any(existing_zone == zone for _, existing_zone in cities):
        messagebox.showinfo(
            "Already added",
            "That time zone is already displayed."
        )
        return

    cities.append((city, zone))
    city_var.set("")
    redraw_clocks()


def remove_city():
    if not cities:
        messagebox.showinfo("No cities", "There are no cities to remove.")
        return

    options = [
        f"{index + 1}. {city} ({zone})"
        for index, (city, zone) in enumerate(cities)
    ]

    picker = tk.Toplevel(root)
    picker.title("Remove a city")
    picker.configure(bg=BG)
    picker.resizable(False, False)
    picker.transient(root)
    picker.grab_set()

    make_label(picker, "Choose a clock to remove", 12, TEXT, True).pack(
        padx=18, pady=(18, 10)
    )

    choice = tk.StringVar(value=options[0])
    ttk.Combobox(
        picker,
        textvariable=choice,
        values=options,
        state="readonly",
        width=36
    ).pack(padx=18, pady=5)

    def confirm_remove():
        selected = options.index(choice.get())
        cities.pop(selected)
        picker.destroy()
        redraw_clocks()

    make_button(
        picker, "Remove selected city", confirm_remove, "#ff8c8c"
    ).pack(padx=18, pady=15)


make_button(city_panel, "＋ Add city", add_city).grid(
    row=1, column=2, sticky="ew"
)

make_button(
    city_panel, "− Remove city", remove_city, "#ffb86b"
).grid(row=3, column=0, columnspan=3, sticky="w", pady=(10, 0))


# ---------- TIME ZONE CONVERTER ----------

converter = tk.Frame(root, bg=PANEL, padx=14, pady=12)
converter.pack(fill="x", padx=28, pady=(0, 18))

make_label(converter, "Time zone converter", 14, TEXT, True).grid(
    row=0, column=0, columnspan=4, sticky="w", pady=(0, 5)
)

make_label(
    converter, "Date (YYYY-MM-DD)", 9, MUTED
).grid(row=1, column=0, sticky="w", pady=(5, 3))

make_label(
    converter, "Time (HH:MM)", 9, MUTED
).grid(row=1, column=1, sticky="w", pady=(5, 3))

date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
time_var = tk.StringVar(value=datetime.now().strftime("%H:%M"))

tk.Entry(
    converter, textvariable=date_var, width=16,
    bg=CARD, fg=TEXT, insertbackground=TEXT,
    relief="flat", font=("Consolas", 10)
).grid(row=2, column=0, sticky="ew", padx=(0, 8), ipady=7)

tk.Entry(
    converter, textvariable=time_var, width=10,
    bg=CARD, fg=TEXT, insertbackground=TEXT,
    relief="flat", font=("Consolas", 10)
).grid(row=2, column=1, sticky="ew", padx=(0, 8), ipady=7)

from_var = tk.StringVar(value="Asia/Bahrain")
to_var = tk.StringVar(value="Europe/London")

make_label(converter, "From", 9, MUTED).grid(
    row=3, column=0, sticky="w", pady=(8, 3)
)
make_label(converter, "To", 9, MUTED).grid(
    row=3, column=1, sticky="w", pady=(8, 3)
)

ttk.Combobox(
    converter, textvariable=from_var,
    values=zone_names, state="readonly", width=25
).grid(row=4, column=0, sticky="ew", padx=(0, 8))

ttk.Combobox(
    converter, textvariable=to_var,
    values=zone_names, state="readonly", width=25
).grid(row=4, column=1, sticky="ew", padx=(0, 8))

result_label = tk.Label(
    converter,
    text="Choose time zones and press Convert.",
    font=("Segoe UI", 10),
    bg=PANEL, fg=GREEN,
    justify="left",
    wraplength=650
)
result_label.grid(
    row=6, column=0, columnspan=4,
    sticky="w", pady=(12, 0)
)


def convert_time():
    try:
        date_text = date_var.get().strip()
        time_text = time_var.get().strip()

        local_time = datetime.strptime(
            f"{date_text} {time_text}", "%Y-%m-%d %H:%M"
        )

        source_zone = ZoneInfo(from_var.get())
        target_zone = ZoneInfo(to_var.get())

        source_time = local_time.replace(tzinfo=source_zone)
        target_time = source_time.astimezone(target_zone)

        result_label.config(
            text=(
                f"{from_var.get()}: "
                f"{source_time.strftime('%A, %d %B %Y at %H:%M')}\n"
                f"{to_var.get()}: "
                f"{target_time.strftime('%A, %d %B %Y at %H:%M')}"
            ),
            fg=GREEN
        )

    except ValueError:
        messagebox.showerror(
            "Invalid date or time",
            "Use YYYY-MM-DD for the date and HH:MM for the time."
        )
    except Exception as error:
        messagebox.showerror(
            "Conversion error", str(error)
        )


make_button(
    converter, "Convert time", convert_time
).grid(row=5, column=0, sticky="w", pady=(10, 0))

make_button(
    converter, "Use current time",
    lambda: (
        date_var.set(datetime.now().strftime("%Y-%m-%d")),
        time_var.set(datetime.now().strftime("%H:%M"))
    ),
    "#65e6b2"
).grid(row=5, column=1, sticky="w", pady=(10, 0))

# Start the application
redraw_clocks()
root.mainloop()
