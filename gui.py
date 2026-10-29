# STATUS
#   Built:  Home page, Check Out page, Customer Account page, Search Movies page
#   Stubs:  Add/Remove Movies page, Check Out Confirmation page (title + Back only)
#   TODO (Sprint 4): connect the buttons to DBInterface, add sorting on the
#                    Search page, finish the two stub pages
#
# Right now the buttons only move between pages or show placeholder text.
# Nothing here talks to the database yet.

import tkinter as tk

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
window = tk.Tk()
window.title("Scrum Team 6 movie store")

# Same idea as the text editor example: minsize sets the starting size and
# weight=1 lets the page grow when the window is resized.
window.rowconfigure(0, minsize=600, weight=1)
window.columnconfigure(0, minsize=1000, weight=1)

# Fonts used for the big page titles
FONT_TITLE = ("Helvetica", 28, "bold")
FONT_HEADING = ("Helvetica", 14, "bold")


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
    show_page(frm_checkout)


def go_customer():
    show_page(frm_customer)


def go_inhouse():
    show_page(frm_inhouse)


def go_search():
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
def lookup_customer():
    customer_id = ent_customer_id.get()
    # TODO (Sprint 4): use db.get_customer_info(int(customer_id)) here
    lbl_customer_name["text"] = f"Name: (customer {customer_id} will show here)"
    lbl_customer_email["text"] = "Email: (email will show here)"


def lookup_movie():
    video_id = ent_video_id.get()
    # TODO (Sprint 4): use db.get_video_info(video_id) here
    lbl_movie_title["text"] = f"Title: (video {video_id} will show here)"
    lbl_movie_details["text"] = "Rating / Genre: (will show here)"
    lbl_movie_stock["text"] = "In stock: (will show here)"


def confirm_checkout():
    # TODO (Sprint 4): use db.new_rental(videoID, customerID, rental_end_date)
    show_page(frm_confirm)


frm_checkout = tk.Frame(master=window)
frm_checkout.columnconfigure(0, weight=1)
frm_checkout.rowconfigure(2, weight=1)

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
ent_video_id = tk.Entry(master=frm_movie_box, width=15)
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
lbl_start_date = tk.Label(master=frm_dates, text="Start date:")
ent_start_date = tk.Entry(master=frm_dates, width=15)
ent_start_date.insert(0, "MM/DD/YYYY")
lbl_end_date = tk.Label(master=frm_dates, text="End date:")
ent_end_date = tk.Entry(master=frm_dates, width=15)
ent_end_date.insert(0, "MM/DD/YYYY")

lbl_dates_heading.grid(row=0, column=0, columnspan=4, pady=5)
lbl_start_date.grid(row=1, column=0, sticky="e")
ent_start_date.grid(row=1, column=1, padx=5)
lbl_end_date.grid(row=1, column=2, sticky="e", padx=(20, 0))
ent_end_date.grid(row=1, column=3, padx=5)
frm_dates.grid(row=1, column=0, columnspan=2, pady=20)

btn_confirm = tk.Button(
    master=frm_checkout_body, text="Confirm Check Out",
    width=25, height=2, command=confirm_checkout
)
btn_confirm.grid(row=2, column=0, columnspan=2, pady=10)

btn_checkout_back = tk.Button(
    master=frm_checkout, text="Back", width=10, command=go_home
)
btn_checkout_back.grid(row=2, column=0, sticky="sw", padx=20, pady=20)


# ======================================================================
# PAGE 3: CREATE / EDIT CUSTOMER ACCOUNT
# ======================================================================
def set_new_mode():
    lbl_customer_mode["text"] = "Mode: New customer"


def set_edit_mode():
    lbl_customer_mode["text"] = "Mode: Edit existing customer"


def clear_customer_form():
    # Entry.delete(0, tk.END) clears everything in an Entry
    for ent in customer_entries:
        ent.delete(0, tk.END)
    lbl_customer_status["text"] = ""


def save_customer():
    # TODO (Sprint 4): use db.add_new_customer(...) or db.edit_customer_info(...)
    lbl_customer_status["text"] = "Save clicked (database not connected yet)"


frm_customer = tk.Frame(master=window)
frm_customer.columnconfigure(0, weight=1)
frm_customer.rowconfigure(5, weight=1)

lbl_customer_title = tk.Label(
    master=frm_customer, text="Customer Account", font=FONT_TITLE
)
lbl_customer_title.grid(row=0, column=0, pady=20)

# New / Edit buttons
frm_customer_mode = tk.Frame(master=frm_customer)
btn_new_customer = tk.Button(
    master=frm_customer_mode, text="New Customer", width=18, command=set_new_mode
)
btn_edit_customer = tk.Button(
    master=frm_customer_mode, text="Edit Existing", width=18, command=set_edit_mode
)
btn_new_customer.grid(row=0, column=0, padx=10)
btn_edit_customer.grid(row=0, column=1, padx=10)
frm_customer_mode.grid(row=1, column=0)

lbl_customer_mode = tk.Label(master=frm_customer, text="Mode: New customer")
lbl_customer_mode.grid(row=2, column=0, pady=10)

# The form: one Label + Entry for each field, made with a loop
frm_customer_form = tk.Frame(master=frm_customer)
customer_fields = ["Customer ID", "First name", "Last name", "Email", "Address"]
customer_entries = []

for i in range(len(customer_fields)):
    lbl_field = tk.Label(master=frm_customer_form, text=customer_fields[i] + ":")
    ent_field = tk.Entry(master=frm_customer_form, width=35)
    lbl_field.grid(row=i, column=0, sticky="e", padx=5, pady=5)
    ent_field.grid(row=i, column=1, padx=5, pady=5)
    customer_entries.append(ent_field)

frm_customer_form.grid(row=3, column=0, pady=10)

# Save / Clear buttons
frm_customer_actions = tk.Frame(master=frm_customer)
btn_save_customer = tk.Button(
    master=frm_customer_actions, text="Save", width=18, height=2, command=save_customer
)
btn_clear_customer = tk.Button(
    master=frm_customer_actions, text="Clear", width=18, height=2,
    command=clear_customer_form
)
btn_save_customer.grid(row=0, column=0, padx=10)
btn_clear_customer.grid(row=0, column=1, padx=10)
frm_customer_actions.grid(row=4, column=0, pady=10)

lbl_customer_status = tk.Label(master=frm_customer, text="")
lbl_customer_status.grid(row=5, column=0, sticky="n")

btn_customer_back = tk.Button(
    master=frm_customer, text="Back", width=10, command=go_home
)
btn_customer_back.grid(row=5, column=0, sticky="sw", padx=20, pady=20)


# ======================================================================
# PAGE 4: SEARCH MOVIES
# ======================================================================
# Fake data for now, in the same order as the Videos.csv columns:
# videoID, name, year, rating, genre, total_stock, current_stock
# TODO (Sprint 4): replace with db.get_all_videos()
sample_movies = [
    ["alien", "Alien", 1979, "R", "Horror", 4, 2],
    ["heat", "Heat", 1995, "R", "Crime", 3, 0],
    ["shrek", "Shrek", 2001, "PG", "Comedy", 5, 3],
    ["thematrix", "The Matrix", 1999, "R", "Sci-Fi", 3, 1],
    ["titanic", "Titanic", 1997, "PG-13", "Drama", 2, 2],
    ["toystory", "Toy Story", 1995, "G", "Family", 5, 3],
]


def search_movies():
    search_text = ent_search.get()
    # TODO (Sprint 4): filter the list using the search text
    lbl_search_status["text"] = f'Searching for "{search_text}"... (not connected yet)'


frm_search = tk.Frame(master=window)
frm_search.columnconfigure(0, weight=1)
frm_search.rowconfigure(4, weight=1)

lbl_search_title = tk.Label(
    master=frm_search, text="Search Movies", font=FONT_TITLE
)
lbl_search_title.grid(row=0, column=0, pady=20)

# Search bar + filter buttons
frm_search_bar = tk.Frame(master=frm_search)
ent_search = tk.Entry(master=frm_search_bar, width=40)
btn_do_search = tk.Button(
    master=frm_search_bar, text="Search", width=10, command=search_movies
)
btn_genre = tk.Button(master=frm_search_bar, text="Genre \u25BC", width=10)
btn_rating = tk.Button(master=frm_search_bar, text="Rating \u25BC", width=10)

ent_search.grid(row=0, column=0, padx=5)
btn_do_search.grid(row=0, column=1, padx=5)
btn_genre.grid(row=0, column=2, padx=(30, 5))
btn_rating.grid(row=0, column=3, padx=5)
frm_search_bar.grid(row=1, column=0)

lbl_search_status = tk.Label(master=frm_search, text="")
lbl_search_status.grid(row=2, column=0, pady=5)

# The movie list: header buttons on row 0, then one row of Labels per movie
frm_table = tk.Frame(master=frm_search)
column_names = ["ID", "Name", "Year", "Rating", "Genre", "Stock"]
column_widths = [14, 28, 8, 8, 14, 8]

# TODO (Sprint 4): make these header buttons sort the list
for col in range(len(column_names)):
    btn_header = tk.Button(
        master=frm_table, text=column_names[col], width=column_widths[col]
    )
    btn_header.grid(row=0, column=col, padx=1, pady=2)

for row in range(len(sample_movies)):
    movie = sample_movies[row]
    stock_text = f"{movie[6]}/{movie[5]}"          # current_stock / total_stock
    row_values = [movie[0], movie[1], movie[2], movie[3], movie[4], stock_text]
    for col in range(len(row_values)):
        lbl_cell = tk.Label(
            master=frm_table, text=row_values[col],
            width=column_widths[col], relief=tk.GROOVE, borderwidth=1
        )
        lbl_cell.grid(row=row + 1, column=col, padx=1, pady=1)

frm_table.grid(row=3, column=0, pady=10)

btn_search_back = tk.Button(
    master=frm_search, text="Back", width=10, command=go_home
)
btn_search_back.grid(row=4, column=0, sticky="sw", padx=20, pady=20)


# ======================================================================
# PAGE 5: ADD / REMOVE MOVIES (stub - still to build)
# ======================================================================
frm_inhouse = tk.Frame(master=window)
frm_inhouse.columnconfigure(0, weight=1)
frm_inhouse.rowconfigure(2, weight=1)

lbl_inhouse_title = tk.Label(
    master=frm_inhouse, text="Add/Remove Movies", font=FONT_TITLE
)
lbl_inhouse_title.grid(row=0, column=0, pady=20)

lbl_inhouse_todo = tk.Label(master=frm_inhouse, text="(page still to be built)")
lbl_inhouse_todo.grid(row=1, column=0, pady=40)

btn_inhouse_back = tk.Button(
    master=frm_inhouse, text="Back", width=10, command=go_home
)
btn_inhouse_back.grid(row=2, column=0, sticky="sw", padx=20, pady=20)


# ======================================================================
# PAGE 6: CHECK OUT CONFIRMATION (stub - still to build)
# ======================================================================
frm_confirm = tk.Frame(master=window)
frm_confirm.columnconfigure(0, weight=1)
frm_confirm.rowconfigure(2, weight=1)

lbl_confirm_title = tk.Label(
    master=frm_confirm, text="Rental Confirmed", font=FONT_TITLE
)
lbl_confirm_title.grid(row=0, column=0, pady=20)

lbl_confirm_todo = tk.Label(master=frm_confirm, text="(page still to be built)")
lbl_confirm_todo.grid(row=1, column=0, pady=40)

btn_confirm_home = tk.Button(
    master=frm_confirm, text="Home", width=10, command=go_home
)
btn_confirm_home.grid(row=2, column=0, sticky="sw", padx=20, pady=20)


# ----------------------------------------------------------------------
# Start the app on the Home page
# ----------------------------------------------------------------------
all_pages = [frm_home, frm_checkout, frm_customer, frm_search, frm_inhouse, frm_confirm]
show_page(frm_home)

window.mainloop()
