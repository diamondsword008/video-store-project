import os
import re
import tkinter as tk
from datetime import datetime

from DBInterface import DBInterface

# DBInterface reads the csv files from the current folder, so make sure we
# are running from the folder that this file is in.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# The backend object. Every page below talks to the csv files through this.
db = DBInterface()

window = tk.Tk()
window.title("Scrum Team 6 Movie Store")

# Same idea as the text editor example: minsize sets the starting size and
# weight=1 lets the page grow when the window is resized.
window.rowconfigure(0, minsize=600, weight=1)
window.columnconfigure(0, minsize=1000, weight=1)

# Fonts
FONT_TITLE = ("Helvetica", 28, "bold")
FONT_HEADING = ("Helvetica", 14, "bold")
FONT_LIST = ("Courier", 10)   # same-width letters so the columns line up


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def make_video_id(text):
    # The backend makes a videoID by removing everything except letters and
    # numbers from the movie's name and making it lowercase.
    # Doing the same here means "The Lego Movie" works as a Video ID.
    return re.sub(r"[^a-zA-Z0-9]", "", text).lower()


def format_date(a_date):
    # The backend stores dates as date objects, so turn them into mm/dd/yyyy
    if isinstance(a_date, str):
        return a_date
    return a_date.strftime("%m/%d/%Y")


# ----------------------------------------------------------------------
# Moving between pages
# Every page is a Frame. show_page() hides all of them, then shows one.
# ----------------------------------------------------------------------
def show_page(frm_page):
    for frm in all_pages:
        frm.grid_remove()
    frm_page.grid(row=0, column=0, sticky="nsew")


# One small function per page so the buttons can use command=
def go_home():
    show_page(frm_home)


def go_checkout():
    clear_checkout_form()
    show_page(frm_checkout)


def go_customer():
    refresh_customer_list()
    lbl_customer_list_status["text"] = ""
    show_page(frm_customer)


def go_inhouse():
    refresh_inhouse_list()
    lbl_inhouse_status["text"] = ""
    show_page(frm_inhouse)


def go_search():
    ent_search.delete(0, tk.END)
    show_movies()
    show_page(frm_search)


# ======================================================================
# PAGE 1: HOME
# ======================================================================
frm_home = tk.Frame(master=window)
frm_home.columnconfigure([0, 1], weight=1)

lbl_welcome = tk.Label(
    master=frm_home,
    text="Welcome to Scrum Team 6!",
    font=FONT_TITLE
)
lbl_question = tk.Label(
    master=frm_home,
    text="What would you like to do today?",
    font=("Helvetica", 16)
)

btn_checkout = tk.Button(
    master=frm_home, text="Check out a movie",
    width=28, height=3, command=go_checkout
)
btn_customer = tk.Button(
    master=frm_home, text="Create/edit customer account",
    width=28, height=3, command=go_customer
)
btn_inhouse = tk.Button(
    master=frm_home, text="Add/remove movies in-house",
    width=28, height=3, command=go_inhouse
)
btn_search = tk.Button(
    master=frm_home, text="Search movies",
    width=28, height=3, command=go_search
)

lbl_welcome.grid(row=0, column=0, columnspan=2, pady=(80, 10))
lbl_question.grid(row=1, column=0, columnspan=2, pady=(0, 40))
btn_checkout.grid(row=2, column=0, padx=10, pady=10, sticky="e")
btn_customer.grid(row=2, column=1, padx=10, pady=10, sticky="w")
btn_inhouse.grid(row=3, column=0, padx=10, pady=10, sticky="e")
btn_search.grid(row=3, column=1, padx=10, pady=10, sticky="w")


# ======================================================================
# PAGE 2: CHECK OUT A MOVIE
# ======================================================================
def clear_checkout_form():
    ent_customer_id.delete(0, tk.END)
    ent_video_id.delete(0, tk.END)
    ent_end_date.delete(0, tk.END)
    lbl_customer_name["text"] = "Name: "
    lbl_customer_email["text"] = "Email: "
    lbl_movie_title["text"] = "Title: "
    lbl_movie_details["text"] = "Rating / Genre: "
    lbl_movie_stock["text"] = "In stock: "
    lbl_start_date["text"] = "Start date: " + datetime.today().strftime("%m/%d/%Y") + " (today)"
    lbl_checkout_status["text"] = ""


def lookup_customer():
    customer_text = ent_customer_id.get().strip()
    lbl_customer_name["text"] = "Name: "
    lbl_customer_email["text"] = "Email: "

    if not customer_text.isdigit():
        lbl_checkout_status["text"] = "Customer ID must be a number."
        return

    customer = db.get_customer_info(int(customer_text))
    if not customer:
        lbl_checkout_status["text"] = "No customer found with that ID."
        return

    # customer = [customerID, first_name, last_name, email, address]
    lbl_customer_name["text"] = f"Name: {customer[1]} {customer[2]}"
    lbl_customer_email["text"] = f"Email: {customer[3]}"
    lbl_checkout_status["text"] = ""


def lookup_movie():
    video_id = make_video_id(ent_video_id.get())
    lbl_movie_title["text"] = "Title: "
    lbl_movie_details["text"] = "Rating / Genre: "
    lbl_movie_stock["text"] = "In stock: "

    video = db.get_video_info(video_id)
    if not video:
        lbl_checkout_status["text"] = "No movie found with that Video ID."
        return

    # video = [videoID, name, year, rating, genre, total_stock, current_stock]
    lbl_movie_title["text"] = f"Title: {video[1]} ({video[2]})"
    lbl_movie_details["text"] = f"Rating / Genre: {video[3]} / {video[4]}"
    lbl_movie_stock["text"] = f"In stock: {video[6]} of {video[5]}"
    lbl_checkout_status["text"] = ""


def confirm_checkout():
    # 1. check the customer
    customer_text = ent_customer_id.get().strip()
    if not customer_text.isdigit():
        lbl_checkout_status["text"] = "Customer ID must be a number."
        return
    customer_id = int(customer_text)
    customer = db.get_customer_info(customer_id)
    if not customer:
        lbl_checkout_status["text"] = "No customer found with that ID."
        return

    # 2. check the movie
    video_id = make_video_id(ent_video_id.get())
    video = db.get_video_info(video_id)
    if not video:
        lbl_checkout_status["text"] = "No movie found with that Video ID."
        return
    if int(video[6]) < 1:
        lbl_checkout_status["text"] = "Sorry, there are no copies of that movie in stock."
        return

    # 3. check the end date (must be mm/dd/yyyy and not in the past)
    try:
        end_date = datetime.strptime(ent_end_date.get().strip(), "%m/%d/%Y")
    except ValueError:
        lbl_checkout_status["text"] = "End date must look like MM/DD/YYYY."
        return
    if end_date.date() < datetime.today().date():
        lbl_checkout_status["text"] = "End date can't be before today."
        return

    # 4. save the rental in the backend (it fills in the start date for us)
    worked = db.new_rental(video_id, customer_id, end_date.strftime("%m/%d/%Y"))
    if not worked:
        lbl_checkout_status["text"] = "The rental could not be saved."
        return

    # new_rental doesn't lower the stock, so we lower it here
    db.edit_video_info(video_id, "current_stock", int(video[6]) - 1)

    # 5. the new rental is the last one in this customer's current rentals
    # rental = [rentalNo, videoID, customerID, start_date, end_date, returned]
    rental = db.get_current_rentals(customer_id)[-1]

    lbl_confirm_rental["text"] = f"Rental #: {rental[0]}"
    lbl_confirm_customer["text"] = f"Customer: {customer[1]} {customer[2]}"
    lbl_confirm_customer_id["text"] = f"Customer ID: {customer[0]}"
    lbl_confirm_movie["text"] = f"Movie: {video[1]} ({video[2]})"
    lbl_confirm_video_id["text"] = f"Video ID: {video[0]}"
    lbl_confirm_start["text"] = f"Start date: {format_date(rental[3])}"
    lbl_confirm_end["text"] = f"Return by: {format_date(rental[4])}"
    lbl_confirm_status["text"] = "Status: Checked out"
    show_page(frm_confirm)


frm_checkout = tk.Frame(master=window)
frm_checkout.columnconfigure(0, weight=1)
frm_checkout.rowconfigure(3, weight=1)

lbl_checkout_title = tk.Label(
    master=frm_checkout, text="Check Out a Movie", font=FONT_TITLE
)
lbl_checkout_title.grid(row=0, column=0, pady=20)

frm_checkout_body = tk.Frame(master=frm_checkout)
frm_checkout_body.grid(row=1, column=0)

# --- Customer section (left side) ---
frm_customer_box = tk.Frame(master=frm_checkout_body)
lbl_customer_heading = tk.Label(
    master=frm_customer_box, text="Customer", font=FONT_HEADING
)
lbl_customer_id = tk.Label(master=frm_customer_box, text="Customer ID:")
ent_customer_id = tk.Entry(master=frm_customer_box, width=15)
btn_lookup_customer = tk.Button(
    master=frm_customer_box, text="Look up", command=lookup_customer
)
lbl_customer_name = tk.Label(master=frm_customer_box, text="Name: ")
lbl_customer_email = tk.Label(master=frm_customer_box, text="Email: ")

lbl_customer_heading.grid(row=0, column=0, columnspan=3, sticky="w", pady=5)
lbl_customer_id.grid(row=1, column=0, sticky="e", pady=5)
ent_customer_id.grid(row=1, column=1, padx=5)
btn_lookup_customer.grid(row=1, column=2)
lbl_customer_name.grid(row=2, column=0, columnspan=3, sticky="w", pady=5)
lbl_customer_email.grid(row=3, column=0, columnspan=3, sticky="w")

# --- Movie section (right side) ---
frm_movie_box = tk.Frame(master=frm_checkout_body)
lbl_movie_heading = tk.Label(
    master=frm_movie_box, text="Movie", font=FONT_HEADING
)
lbl_video_id = tk.Label(master=frm_movie_box, text="Video ID:")
ent_video_id = tk.Entry(master=frm_movie_box, width=25)
btn_lookup_movie = tk.Button(
    master=frm_movie_box, text="Look up", command=lookup_movie
)
lbl_movie_title = tk.Label(master=frm_movie_box, text="Title: ")
lbl_movie_details = tk.Label(master=frm_movie_box, text="Rating / Genre: ")
lbl_movie_stock = tk.Label(master=frm_movie_box, text="In stock: ")

lbl_movie_heading.grid(row=0, column=0, columnspan=3, sticky="w", pady=5)
lbl_video_id.grid(row=1, column=0, sticky="e", pady=5)
ent_video_id.grid(row=1, column=1, padx=5)
btn_lookup_movie.grid(row=1, column=2)
lbl_movie_title.grid(row=2, column=0, columnspan=3, sticky="w", pady=5)
lbl_movie_details.grid(row=3, column=0, columnspan=3, sticky="w")
lbl_movie_stock.grid(row=4, column=0, columnspan=3, sticky="w", pady=5)

frm_customer_box.grid(row=0, column=0, padx=60, pady=10, sticky="n")
frm_movie_box.grid(row=0, column=1, padx=60, pady=10, sticky="n")

# --- Rental dates (bottom) ---
frm_dates = tk.Frame(master=frm_checkout_body)
lbl_dates_heading = tk.Label(
    master=frm_dates, text="Rental dates", font=FONT_HEADING
)
lbl_start_date = tk.Label(master=frm_dates, text="Start date: ")
lbl_end_date = tk.Label(master=frm_dates, text="End date (MM/DD/YYYY):")
ent_end_date = tk.Entry(master=frm_dates, width=15)

lbl_dates_heading.grid(row=0, column=0, columnspan=3, pady=5)
lbl_start_date.grid(row=1, column=0, sticky="e", padx=(0, 30))
lbl_end_date.grid(row=1, column=1, sticky="e")
ent_end_date.grid(row=1, column=2, padx=5)
frm_dates.grid(row=1, column=0, columnspan=2, pady=20)

btn_confirm = tk.Button(
    master=frm_checkout_body, text="Confirm Check Out",
    width=25, height=2, command=confirm_checkout
)
btn_confirm.grid(row=2, column=0, columnspan=2, pady=10)

lbl_checkout_status = tk.Label(master=frm_checkout, text="", fg="red")
lbl_checkout_status.grid(row=2, column=0)

btn_checkout_back = tk.Button(
    master=frm_checkout, text="Back", width=10, command=go_home
)
btn_checkout_back.grid(row=3, column=0, sticky="sw", padx=20, pady=20)


# ======================================================================
# PAGE 3: CUSTOMERS (the list) and PAGE 3b: CUSTOMER FORM (new / edit)
# ======================================================================
customer_rows = []            # the customers in the list, in the same order
editing_customer_id = None    # None means we are adding a new customer


def refresh_customer_list():
    global customer_rows
    customer_rows = db.get_all_customers()
    lst_customers.delete(0, tk.END)
    for c in customer_rows:
        # c = [customerID, first_name, last_name, email, address]
        line = f"{c[0]:<5}{c[1]:<14}{c[2]:<14}{c[3]:<28}{c[4]}"
        lst_customers.insert(tk.END, line)


def edit_selected_customer():
    selection = lst_customers.curselection()
    if len(selection) == 0:
        lbl_customer_list_status["text"] = "Click a customer in the list first."
        return
    open_customer_form(customer_rows[selection[0]])


def new_customer():
    open_customer_form(None)


def open_customer_form(customer):
    global editing_customer_id
    for key in customer_keys:
        ent_customer[key].delete(0, tk.END)
    lbl_customer_form_status["text"] = ""

    if customer is None:
        editing_customer_id = None
        lbl_customer_form_title["text"] = "New Customer"
        lbl_customer_form_id["text"] = "Customer ID: (made automatically)"
    else:
        editing_customer_id = customer[0]
        lbl_customer_form_title["text"] = "Edit Customer"
        lbl_customer_form_id["text"] = f"Customer ID: {customer[0]}"
        # fill the boxes with what is already saved, so only the
        # things that change need to be typed
        for i in range(len(customer_keys)):
            ent_customer[customer_keys[i]].insert(0, customer[i + 1])
    show_page(frm_customer_form)


def save_customer():
    values = {}
    for key in customer_keys:
        values[key] = ent_customer[key].get().strip()
        if values[key] == "":
            lbl_customer_form_status["text"] = "Please fill in every box."
            return
    if "@" not in values["email"]:
        lbl_customer_form_status["text"] = "The email needs an @ in it."
        return

    if editing_customer_id is None:
        # The backend does not check for duplicates, so check the email here
        for c in db.get_all_customers():
            if c[3].lower() == values["email"].lower():
                lbl_customer_form_status["text"] = "A customer with that email already exists."
                return
        db.add_new_customer(
            values["first_name"], values["last_name"],
            values["email"], values["address"]
        )
        message = "New customer added."
    else:
        # only send the backend the things that were changed
        old = db.get_customer_info(editing_customer_id)
        for i in range(len(customer_keys)):
            key = customer_keys[i]
            if values[key] != old[i + 1]:
                db.edit_customer_info(editing_customer_id, key, values[key])
        message = "Customer updated."

    refresh_customer_list()
    lbl_customer_list_status["text"] = message
    show_page(frm_customer)


def cancel_customer_form():
    lbl_customer_list_status["text"] = ""
    show_page(frm_customer)


# --- The list page ---
frm_customer = tk.Frame(master=window)
frm_customer.columnconfigure(0, weight=1)
frm_customer.rowconfigure(5, weight=1)

lbl_customer_title = tk.Label(
    master=frm_customer, text="Customers", font=FONT_TITLE
)
lbl_customer_title.grid(row=0, column=0, pady=20)

lbl_customer_hint = tk.Label(
    master=frm_customer,
    text="Click a customer to select them, then press Edit Selected."
)
lbl_customer_hint.grid(row=1, column=0)

frm_customer_list = tk.Frame(master=frm_customer)
lbl_customer_header = tk.Label(
    master=frm_customer_list,
    text=f"{'ID':<5}{'First name':<14}{'Last name':<14}{'Email':<28}Address",
    font=FONT_LIST, anchor="w"
)
lst_customers = tk.Listbox(
    master=frm_customer_list, width=100, height=10, font=FONT_LIST,
    exportselection=False
)
scr_customers = tk.Scrollbar(master=frm_customer_list, command=lst_customers.yview)
lst_customers["yscrollcommand"] = scr_customers.set

lbl_customer_header.grid(row=0, column=0, sticky="w")
lst_customers.grid(row=1, column=0)
scr_customers.grid(row=1, column=1, sticky="ns")
frm_customer_list.grid(row=2, column=0, pady=10)

frm_customer_actions = tk.Frame(master=frm_customer)
btn_edit_customer = tk.Button(
    master=frm_customer_actions, text="Edit Selected", width=18, height=2,
    command=edit_selected_customer
)
btn_new_customer = tk.Button(
    master=frm_customer_actions, text="New Customer", width=18, height=2,
    command=new_customer
)
btn_edit_customer.grid(row=0, column=0, padx=10)
btn_new_customer.grid(row=0, column=1, padx=10)
frm_customer_actions.grid(row=3, column=0, pady=10)

lbl_customer_list_status = tk.Label(master=frm_customer, text="")
lbl_customer_list_status.grid(row=4, column=0)

btn_customer_back = tk.Button(
    master=frm_customer, text="Back", width=10, command=go_home
)
btn_customer_back.grid(row=5, column=0, sticky="sw", padx=20, pady=20)

# --- The form page (used for both new and edit) ---
frm_customer_form = tk.Frame(master=window)
frm_customer_form.columnconfigure(0, weight=1)
frm_customer_form.rowconfigure(4, weight=1)

lbl_customer_form_title = tk.Label(
    master=frm_customer_form, text="New Customer", font=FONT_TITLE
)
lbl_customer_form_title.grid(row=0, column=0, pady=20)

lbl_customer_form_id = tk.Label(master=frm_customer_form, text="Customer ID: ")
lbl_customer_form_id.grid(row=1, column=0, pady=5)

# One Label + Entry for each field, made with a loop.
# ent_customer is a dictionary so each Entry can be found by its field name.
frm_customer_fields = tk.Frame(master=frm_customer_form)
customer_keys = ["first_name", "last_name", "email", "address"]
customer_labels = ["First name:", "Last name:", "Email:", "Address:"]
ent_customer = {}

for i in range(len(customer_keys)):
    lbl_field = tk.Label(master=frm_customer_fields, text=customer_labels[i])
    ent_field = tk.Entry(master=frm_customer_fields, width=40)
    lbl_field.grid(row=i, column=0, sticky="e", padx=5, pady=5)
    ent_field.grid(row=i, column=1, padx=5, pady=5)
    ent_customer[customer_keys[i]] = ent_field

frm_customer_fields.grid(row=2, column=0, pady=10)

frm_customer_form_actions = tk.Frame(master=frm_customer_form)
btn_save_customer = tk.Button(
    master=frm_customer_form_actions, text="Save", width=18, height=2,
    command=save_customer
)
btn_cancel_customer = tk.Button(
    master=frm_customer_form_actions, text="Cancel", width=18, height=2,
    command=cancel_customer_form
)
btn_save_customer.grid(row=0, column=0, padx=10)
btn_cancel_customer.grid(row=0, column=1, padx=10)
frm_customer_form_actions.grid(row=3, column=0, pady=10)

lbl_customer_form_status = tk.Label(master=frm_customer_form, text="", fg="red")
lbl_customer_form_status.grid(row=4, column=0, sticky="n")


# ======================================================================
# PAGE 4: SEARCH MOVIES
# ======================================================================
column_names = ["ID", "Name", "Year", "Rating", "Genre", "Stock"]
column_widths = [24, 32, 8, 8, 12, 8]
MAX_ROWS = 10             # how many movies fit on the page

sort_column = 1           # which column the list is sorted by (0 = ID, 1 = Name ...)
sort_ascending = True


def sort_value(video):
    # video = [videoID, name, year, rating, genre, total_stock, current_stock]
    if sort_column == 0:
        return video[0]
    if sort_column == 1:
        return video[1].lower()
    if sort_column == 2:
        return video[2]
    if sort_column == 3:
        # sort ratings in the backend's order (NC-17, R, PG-13, PG, G)
        if video[3] in db.rating_categories:
            return db.rating_categories.index(video[3])
        return 99
    if sort_column == 4:
        return video[4].lower()
    return video[6]       # Stock: sort by how many are in stock right now


def sort_movies(column):
    global sort_column, sort_ascending
    if column == sort_column:
        sort_ascending = not sort_ascending     # same header again: flip it
    else:
        sort_column = column
        sort_ascending = True
    show_movies()


def show_movies():
    search_text = ent_search.get().strip().lower()

    # get every movie from the backend (movies that were removed have 0 stock)
    movies = []
    for video in db.get_all_videos():
        if int(video[5]) == 0:
            continue
        if search_text == "" or search_text in video[1].lower() or search_text in video[4].lower():
            movies.append(video)

    movies.sort(key=sort_value, reverse=not sort_ascending)

    # show an arrow on the header of the column the list is sorted by
    for col in range(len(column_names)):
        header_text = column_names[col]
        if col == sort_column:
            if sort_ascending:
                header_text = header_text + " \u25B2"
            else:
                header_text = header_text + " \u25BC"
        btn_headers[col]["text"] = header_text

    # throw away the old rows, then make a new row of Labels for each movie
    for widget in frm_table_rows.winfo_children():
        widget.destroy()

    shown = movies[:MAX_ROWS]
    for row in range(len(shown)):
        video = shown[row]
        stock_text = f"{video[6]}/{video[5]}"      # current_stock / total_stock
        row_values = [video[0], video[1], video[2], video[3], video[4], stock_text]
        for col in range(len(row_values)):
            lbl_cell = tk.Label(
                master=frm_table_rows, text=row_values[col],
                width=column_widths[col], relief=tk.GROOVE, borderwidth=1
            )
            lbl_cell.grid(row=row, column=col, padx=1, pady=1)

    if len(movies) == 0:
        lbl_search_status["text"] = "No movies found."
    elif len(movies) > MAX_ROWS:
        lbl_search_status["text"] = f"{len(movies)} movies found (showing the first {MAX_ROWS})"
    else:
        lbl_search_status["text"] = f"{len(movies)} movie(s) found"


frm_search = tk.Frame(master=window)
frm_search.columnconfigure(0, weight=1)
frm_search.rowconfigure(4, weight=1)

lbl_search_title = tk.Label(
    master=frm_search, text="Search Movies", font=FONT_TITLE
)
lbl_search_title.grid(row=0, column=0, pady=20)

# Search bar (you can search by title or genre)
frm_search_bar = tk.Frame(master=frm_search)
ent_search = tk.Entry(master=frm_search_bar, width=40)
btn_do_search = tk.Button(
    master=frm_search_bar, text="Search", width=10, command=show_movies
)
ent_search.grid(row=0, column=0, padx=5)
btn_do_search.grid(row=0, column=1, padx=5)
frm_search_bar.grid(row=1, column=0)

lbl_search_status = tk.Label(master=frm_search, text="")
lbl_search_status.grid(row=2, column=0, pady=5)

# The movie list: header buttons on top, one row of Labels per movie below
frm_table = tk.Frame(master=frm_search)
frm_table_header = tk.Frame(master=frm_table)
frm_table_rows = tk.Frame(master=frm_table)
btn_headers = []

for col in range(len(column_names)):
    # command needs to know which column was clicked, so a small lambda is used
    btn_header = tk.Button(
        master=frm_table_header, text=column_names[col], width=column_widths[col],
        command=lambda c=col: sort_movies(c)
    )
    btn_header.grid(row=0, column=col, padx=1, pady=2)
    btn_headers.append(btn_header)

frm_table_header.grid(row=0, column=0)
frm_table_rows.grid(row=1, column=0)
frm_table.grid(row=3, column=0, pady=10)

btn_search_back = tk.Button(
    master=frm_search, text="Back", width=10, command=go_home
)
btn_search_back.grid(row=4, column=0, sticky="sw", padx=20, pady=20)


# ======================================================================
# PAGE 5: ADD / REMOVE MOVIES
# ======================================================================
inhouse_rows = []             # the movies in the list, in the same order


def refresh_inhouse_list():
    global inhouse_rows
    inhouse_rows = []
    lst_inhouse.delete(0, tk.END)
    for video in db.get_all_videos():
        # removed movies have 0 stock, so skip them
        if int(video[5]) > 0:
            inhouse_rows.append(video)
            line = f"{video[1]:<34}{video[2]:<6}{video[3]:<7}{video[6]}/{video[5]}"
            lst_inhouse.insert(tk.END, line)


def add_movie():
    name = ent_new_name.get().strip()
    year_text = ent_new_year.get().strip()
    rating = ent_new_rating.get().strip().upper()
    genre = ent_new_genre.get().strip()
    stock_text = ent_new_stock.get().strip()

    if name == "" or genre == "" or rating == "":
        lbl_inhouse_status["text"] = "Please fill in every box."
        return
    if not year_text.isdigit() or not stock_text.isdigit():
        lbl_inhouse_status["text"] = "Year and total stock must be numbers."
        return
    year = int(year_text)
    stock = int(stock_text)
    if year < 1888 or year > 2100:
        lbl_inhouse_status["text"] = "Please enter a real year."
        return
    if stock < 1:
        lbl_inhouse_status["text"] = "Total stock must be at least 1."
        return
    if rating not in db.rating_categories:
        lbl_inhouse_status["text"] = "Rating must be one of: " + ", ".join(db.rating_categories)
        return

    video_id = make_video_id(name)
    if video_id == "":
        lbl_inhouse_status["text"] = "The name needs some letters or numbers."
        return

    existing = db.get_video_info(video_id)
    if existing and int(existing[5]) > 0:
        lbl_inhouse_status["text"] = "That movie is already in the store. Select it in the list to add stock."
        return

    if existing:
        # The movie was removed before (its stock was set to 0), so bring it back
        db.edit_video_info(video_id, "year", year)
        db.edit_video_info(video_id, "rating", rating)
        db.edit_video_info(video_id, "genre", genre)
        worked = db.add_stock(video_id, stock)
    else:
        worked = db.add_new_video(name, year, rating, genre, stock)

    if not worked:
        lbl_inhouse_status["text"] = "The movie could not be added."
        return

    for ent in [ent_new_name, ent_new_year, ent_new_rating, ent_new_genre, ent_new_stock]:
        ent.delete(0, tk.END)
    refresh_inhouse_list()
    lbl_inhouse_status["text"] = f'Added "{name}" to the store.'


def add_stock_to_selected():
    selection = lst_inhouse.curselection()
    if len(selection) == 0:
        lbl_inhouse_status["text"] = "Click a movie in the list first."
        return
    amount_text = ent_add_stock.get().strip()
    if not amount_text.isdigit() or int(amount_text) < 1:
        lbl_inhouse_status["text"] = "Enter a number of copies (1 or more)."
        return

    video = inhouse_rows[selection[0]]
    if db.add_stock(video[0], int(amount_text)):
        refresh_inhouse_list()
        lbl_inhouse_status["text"] = f'Added {amount_text} copies of "{video[1]}".'
    else:
        lbl_inhouse_status["text"] = "The stock could not be added."


def remove_selected_movie():
    selection = lst_inhouse.curselection()
    if len(selection) == 0:
        lbl_inhouse_status["text"] = "Click a movie in the list first."
        return

    video = inhouse_rows[selection[0]]
    if db.delete_video(video[0]):
        refresh_inhouse_list()
        lbl_inhouse_status["text"] = f'Removed "{video[1]}" from the store.'
    else:
        lbl_inhouse_status["text"] = f'Could not remove "{video[1]}" because someone is still renting it.'


frm_inhouse = tk.Frame(master=window)
frm_inhouse.columnconfigure(0, weight=1)
frm_inhouse.rowconfigure(3, weight=1)

lbl_inhouse_title = tk.Label(
    master=frm_inhouse, text="Add/Remove Movies", font=FONT_TITLE
)
lbl_inhouse_title.grid(row=0, column=0, pady=20)

frm_inhouse_body = tk.Frame(master=frm_inhouse)
frm_inhouse_body.grid(row=1, column=0)

# --- Left side: add a new movie ---
frm_add_box = tk.Frame(master=frm_inhouse_body)
lbl_add_heading = tk.Label(
    master=frm_add_box, text="Add a new movie", font=FONT_HEADING
)
lbl_add_heading.grid(row=0, column=0, columnspan=2, sticky="w", pady=5)

lbl_new_name = tk.Label(master=frm_add_box, text="Name:")
ent_new_name = tk.Entry(master=frm_add_box, width=28)
lbl_new_year = tk.Label(master=frm_add_box, text="Year:")
ent_new_year = tk.Entry(master=frm_add_box, width=28)
lbl_new_rating = tk.Label(master=frm_add_box, text="Rating:")
ent_new_rating = tk.Entry(master=frm_add_box, width=28)
lbl_rating_hint = tk.Label(
    master=frm_add_box, text="(NC-17, R, PG-13, PG or G)", font=("Helvetica", 8)
)
lbl_new_genre = tk.Label(master=frm_add_box, text="Genre:")
ent_new_genre = tk.Entry(master=frm_add_box, width=28)
lbl_new_stock = tk.Label(master=frm_add_box, text="Total stock:")
ent_new_stock = tk.Entry(master=frm_add_box, width=28)
btn_add_movie = tk.Button(
    master=frm_add_box, text="Add Movie", width=20, height=2, command=add_movie
)

lbl_new_name.grid(row=1, column=0, sticky="e", pady=4)
ent_new_name.grid(row=1, column=1, padx=5)
lbl_new_year.grid(row=2, column=0, sticky="e", pady=4)
ent_new_year.grid(row=2, column=1, padx=5)
lbl_new_rating.grid(row=3, column=0, sticky="e", pady=4)
ent_new_rating.grid(row=3, column=1, padx=5)
lbl_rating_hint.grid(row=4, column=1, sticky="w", padx=5)
lbl_new_genre.grid(row=5, column=0, sticky="e", pady=4)
ent_new_genre.grid(row=5, column=1, padx=5)
lbl_new_stock.grid(row=6, column=0, sticky="e", pady=4)
ent_new_stock.grid(row=6, column=1, padx=5)
btn_add_movie.grid(row=7, column=0, columnspan=2, pady=15)

# --- Right side: the movies in the store (add stock / remove) ---
frm_stock_box = tk.Frame(master=frm_inhouse_body)
lbl_stock_heading = tk.Label(
    master=frm_stock_box, text="Movies in the store", font=FONT_HEADING
)
lbl_stock_heading.grid(row=0, column=0, columnspan=2, sticky="w", pady=5)

lbl_inhouse_header = tk.Label(
    master=frm_stock_box,
    text=f"{'Name':<34}{'Year':<6}{'Rating':<7}Stock",
    font=FONT_LIST, anchor="w"
)
lst_inhouse = tk.Listbox(
    master=frm_stock_box, width=58, height=9, font=FONT_LIST,
    exportselection=False   # keeps the selection when you click in another box
)
scr_inhouse = tk.Scrollbar(master=frm_stock_box, command=lst_inhouse.yview)
lst_inhouse["yscrollcommand"] = scr_inhouse.set

lbl_inhouse_header.grid(row=1, column=0, sticky="w")
lst_inhouse.grid(row=2, column=0)
scr_inhouse.grid(row=2, column=1, sticky="ns")

frm_stock_actions = tk.Frame(master=frm_stock_box)
lbl_add_stock = tk.Label(master=frm_stock_actions, text="Copies to add:")
ent_add_stock = tk.Entry(master=frm_stock_actions, width=6)
ent_add_stock.insert(0, "1")
btn_add_stock = tk.Button(
    master=frm_stock_actions, text="Add Stock to Selected", width=22,
    command=add_stock_to_selected
)
btn_remove_movie = tk.Button(
    master=frm_stock_actions, text="Remove Selected Movie", width=22,
    command=remove_selected_movie
)
lbl_add_stock.grid(row=0, column=0, sticky="e")
ent_add_stock.grid(row=0, column=1, padx=5)
btn_add_stock.grid(row=0, column=2, padx=5)
btn_remove_movie.grid(row=0, column=3, padx=5)
frm_stock_actions.grid(row=3, column=0, columnspan=2, pady=10)

frm_add_box.grid(row=0, column=0, padx=30, pady=5, sticky="n")
frm_stock_box.grid(row=0, column=1, padx=30, pady=5, sticky="n")

lbl_inhouse_status = tk.Label(master=frm_inhouse, text="")
lbl_inhouse_status.grid(row=2, column=0)

btn_inhouse_back = tk.Button(
    master=frm_inhouse, text="Back", width=10, command=go_home
)
btn_inhouse_back.grid(row=3, column=0, sticky="sw", padx=20, pady=20)


# ======================================================================
# PAGE 6: CHECK OUT CONFIRMATION
# ======================================================================
frm_confirm = tk.Frame(master=window)
frm_confirm.columnconfigure(0, weight=1)
frm_confirm.rowconfigure(3, weight=1)

lbl_confirm_title = tk.Label(
    master=frm_confirm, text="Rental Confirmed", font=FONT_TITLE
)
lbl_confirm_title.grid(row=0, column=0, pady=20)

# The receipt box (these Labels get filled in by confirm_checkout)
frm_receipt = tk.Frame(master=frm_confirm, relief=tk.RIDGE, borderwidth=3)
lbl_confirm_rental = tk.Label(master=frm_receipt, text="Rental #: ", font=FONT_HEADING)
lbl_confirm_customer = tk.Label(master=frm_receipt, text="Customer: ")
lbl_confirm_customer_id = tk.Label(master=frm_receipt, text="Customer ID: ")
lbl_confirm_movie = tk.Label(master=frm_receipt, text="Movie: ")
lbl_confirm_video_id = tk.Label(master=frm_receipt, text="Video ID: ")
lbl_confirm_start = tk.Label(master=frm_receipt, text="Start date: ")
lbl_confirm_end = tk.Label(master=frm_receipt, text="Return by: ")
lbl_confirm_status = tk.Label(master=frm_receipt, text="Status: ")

receipt_labels = [
    lbl_confirm_rental, lbl_confirm_customer, lbl_confirm_customer_id,
    lbl_confirm_movie, lbl_confirm_video_id, lbl_confirm_start,
    lbl_confirm_end, lbl_confirm_status
]
for i in range(len(receipt_labels)):
    receipt_labels[i].grid(row=i, column=0, sticky="w", padx=30, pady=3)
frm_receipt.grid(row=1, column=0, pady=10)

frm_confirm_actions = tk.Frame(master=frm_confirm)
btn_new_checkout = tk.Button(
    master=frm_confirm_actions, text="New Check Out", width=18, height=2,
    command=go_checkout
)
btn_confirm_home = tk.Button(
    master=frm_confirm_actions, text="Home", width=18, height=2, command=go_home
)
btn_new_checkout.grid(row=0, column=0, padx=10)
btn_confirm_home.grid(row=0, column=1, padx=10)
frm_confirm_actions.grid(row=2, column=0, pady=20)


# ----------------------------------------------------------------------
# Start the app on the Home page
# ----------------------------------------------------------------------
all_pages = [
    frm_home, frm_checkout, frm_customer, frm_customer_form,
    frm_search, frm_inhouse, frm_confirm
]
show_page(frm_home)

window.mainloop()