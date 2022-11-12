import tkinter as tk
from tkinter import *
from tkinter import ttk
import requests
import z_scraper
import webbrowser
import pandas as pd
import os
import Pmw
import json
import time


# --- functions ---
def search():
    # global zip_val
    search_zip = search_entry.get()
    scrape = z_scraper.ZScraper()
    # start = time.time()
    data = scrape.run(search_zip)
    load_data(data)
    # end = time.time()
    # print("Scrape time: ", (end - start))


# fix this method
def save_favorites():
    favorites.append(tv1.set(tv1.focus()))
    fv = pd.DataFrame(favorites)
    fv.to_excel('rentals.xlsx', header=False, index=False)
    popup_msg("The listing was saved")


def reload_favorites():
    if exists:
        fvl = pd.read_excel('rentals.xlsx', header=None)
        data_rows = fvl.to_numpy().tolist()
        for row in data_rows:
            favorites.append(row)


def popup_msg(msg):
    popup = tk.Tk()
    popup.geometry("200x100")
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg)
    label.pack(side=TOP, fill=X, pady=10)
    ok_button = ttk.Button(popup, text="OK", command=popup.destroy)
    ok_button.pack()


def favorites_list():
    favorites_window = Toplevel(root, bg="white")
    favorites_window.title("My favorites")
    favorites_window.geometry("600x400")
    my_favorites_frame = tk.LabelFrame(favorites_window, width=1200, height=225, bg="white")
    my_favorites_frame.pack(pady=30)
    my_favorites_frame.pack_propagate(0)

    fv1 = ttk.Treeview(my_favorites_frame)
    fv1.place(relheight=1, relwidth=1)

    faves_scroll_y = tk.Scrollbar(my_favorites_frame, orient="vertical", command=fv1.yview)
    faves_scroll_x = tk.Scrollbar(my_favorites_frame, orient="horizontal", command=fv1.xview)
    fv1.configure(xscrollcommand=faves_scroll_x.set, yscrollcommand=faves_scroll_y.set)
    faves_scroll_x.pack(side="bottom", fill="x")
    faves_scroll_y.pack(side="right", fill="y")

    # load favorites column headings
    df = pd.DataFrame(favorites)
    fv1["column"] = tv1["columns"]
    fv1["show"] = "headings"

    for column in fv1["columns"]:
        fv1.heading(column, text=column)

    df_rows = df.to_numpy().tolist()
    for row in df_rows:
        print("fav ", row)
        fv1.insert("", "end", values=row)

    fv1.bind("<Double-1>", favOnDoubleClick)


def onDoubleClick(event):
    cur_item = tv1.item(tv1.focus())
    item = tv1.identify('item', event.x, event.y)
    zip_info = get_zip_info()

    # popup window
    listing_window = Toplevel(root, bg="white")
    listing_window.title("Listing detail")
    listing_window.geometry("600x400")
    listing_window_frame = tk.Frame(listing_window, bg="white", height=100)
    listing_window_frame.pack(fill=X, expand=False)

    # listing_window_bg = tk.Frame(listing_window, bg="white")
    Label(listing_window_frame, text=cur_item['values'][0], bg="white").pack(pady=10, side=TOP, anchor='w')
    Label(listing_window_frame, text="square footage: " + cur_item['values'][1], bg="white").pack(pady=2, side=TOP, anchor='w')
    Label(listing_window_frame, text="price: " + cur_item['values'][2], bg="white").pack(pady=2, side=TOP, anchor='w')

    # url link in window
    link = Label(listing_window, text=cur_item['values'][3], bg="white", cursor="hand2")
    link.pack(pady=2, side=TOP, anchor='w')
    link.bind("<Button-1>", lambda e: callback(cur_item['values'][3]))

    # microservice data
    zipc = Label(listing_window_frame, text="", bg="white")
    zipc['text'] = '\n'.join('{} {}'.format(k, d) for k, d in zip_info.items())
    zipc.pack(pady=2, side=BOTTOM, anchor='w')

    # button here to save listing to favorites
    save_to_favorites_button = tk.Button(listing_window_frame, text="Save", font=small_font, bg=favorites_color,
                                              fg="white", command=save_favorites)
    save_to_favorites_button.pack(side=TOP, padx=5, pady=10, anchor='e')

    # Balloons (Tooltips)
    favoritesToolTips = Pmw.Balloon(listing_window_frame)
    favoritesToolTips.bind(save_to_favorites_button, "Click to save to your favorites list")


# Partner microservice API
def get_zip_info():
    zipcode = search_entry.get()
    response = requests.get("https://shaoxi-cs361-microservice.uc.r.appspot.com/"+zipcode).text
    response_info = json.loads(response)

    # city_state, county, population, median_age, median_household_income_by_dollar
    # or primary city, county, timezone, lat/long, estimated population
    county = response_info['county']
    population = response_info['irs_estimated_population']
    timezone = response_info['timezone']
    area_code = response_info['area_codes']

    # city_state = 'Yorktown, VA'
    # county = 'York'
    # population = '124,000'
    # median_age = '32'
    # median_income = '$46,000'

    zip_info = {'County:': county, 'Population:': population, 'Time zone:': timezone,
                'Area code:': area_code}

    return zip_info


def favOnDoubleClick(event):
    cur_item = tv1.item(tv1.focus())
    item = tv1.identify('item', event.x, event.y)

    # popup window
    listing_window = Toplevel(root, bg="white")
    listing_window.title("Listing detail")
    listing_window.geometry("600x400")
    listing_window_frame = tk.Frame(listing_window, bg="white", height=100)
    listing_window_frame.pack(fill=X, expand=False)

    # listing_window_bg = tk.Frame(listing_window, bg="white")
    Label(listing_window_frame, text=cur_item['values'][0], bg="white").pack(pady=10, side=TOP, anchor='w')
    Label(listing_window_frame, text="square footage: " + cur_item['values'][1], bg="white").pack(pady=2, side=TOP,
                                                                                                  anchor='w')
    Label(listing_window_frame, text="price: " + cur_item['values'][2], bg="white").pack(pady=2, side=TOP, anchor='w')

    # url link in window
    link = Label(listing_window, text=cur_item['values'][3], bg="white", cursor="hand2")
    link.pack(pady=2, side=TOP, anchor='w')
    link.bind("<Button-1>", lambda e: callback(cur_item['values'][3]))

    delete_favorite_button = tk.Button(listing_window_frame, text="Delete", font=small_font, bg=delete_color,
                                            fg="white", command=delete_favorite)
    delete_favorite_button.pack(side=TOP, padx=5, pady=10, anchor='e')


def delete_favorite():
    popup_msg("You have chosen to delete this listing.\nThis action cannot be undone.")
    # selected_item = fv1.item(fv1.focus())
    # fv1.delete(selected_item)


def callback(url):
    webbrowser.open_new(url)


def load_data(data):
    clear_data()
    tv1["column"] = list(data.columns)
    tv1["show"] = "headings"

    # assign headings as column names
    for column in tv1["columns"]:
        tv1.heading(column, text=column)

    data_rows = data.to_numpy().tolist()
    for row in data_rows:
        tv1.insert("", "end", values=row)

    # double-click event binding added
    tv1.bind("<Double-1>", onDoubleClick)


def clear_data():
    tv1.delete(*tv1.get_children())


# --- main ---
favorites = []
exists = os.path.isfile('rentals.xlsx')
root = tk.Tk()
root.title("Padmapper")
root.geometry("800x400")
root.resizable(0, 0)
search_zip = tk.StringVar()

Pmw.initialise(root)

# define fonts and colors
search_color = "#f58509"
favorites_color = "#e90c57"
delete_color = "#d92222"
input_color = "#"
large_font = ("SimSun", 14)
small_font = ("SimSun", 10)

search_frame = tk.Frame(root, bg="white", height=100)
search_frame.pack(fill=X, expand=False)

input_frame = tk.LabelFrame(search_frame, text="Enter the zip code to search", bg=search_color, bd=0, fg="white", width=100)
input_frame.pack(pady=10, padx=10, side=LEFT)

favorites_frame = tk.LabelFrame(search_frame, text="My favorites", bg=favorites_color, bd=0,  fg="white", width=150, height=40)
favorites_frame.pack(pady=10, padx=10, side=RIGHT)

output_bg = tk.Frame(root, bg="white")
output_frame = tk.LabelFrame(output_bg, text="Search results", width=1200, height=225)
output_frame.pack(padx=5, pady=30)
output_frame.pack_propagate(0)
output_bg.pack(fill=BOTH, expand=True)

# Search Treeview
tv1 = ttk.Treeview(output_frame)
tv1.place(relheight=1, relwidth=1)

tree_scroll_y = tk.Scrollbar(output_frame, orient="vertical", command=tv1.yview)
tree_scroll_x = tk.Scrollbar(output_frame, orient="horizontal", command=tv1.xview)
tv1.configure(xscrollcommand=tree_scroll_x.set, yscrollcommand=tree_scroll_y.set)
tree_scroll_x.pack(side="bottom", fill="x")
tree_scroll_y.pack(side="right", fill="y")

# reload favorites when program opens
reload_favorites()

# input frame layout
search_entry = ttk.Entry(input_frame, width=20, textvariable=search_zip)
search_button = tk.Button(input_frame, text="Search", font=small_font, bg=search_color, fg="white", command=search)
search_entry.focus()

favorites_button = tk.Button(favorites_frame, text="View", font=small_font, bg=favorites_color, fg="white", command=favorites_list)

end_program_button = tk.Button(output_bg, text="End program", font=small_font, fg="black", command=root.destroy)
end_program_button.pack(padx=5, side="left", expand=False)

# output frame layout
# table = pd.Table(output_frame, dataframe=data)
# table.show()

# implement city search?
# search_method = IntVar()
# search_method.set(1)
# search_city = tk.Radiobutton(input_frame, text="Search city", variable=search_method, value=1)
# search_zip = tk.Radiobutton(input_frame, text="Search zip code", variable=search_method, value=2)

search_entry.grid(row=0, column=0, padx=10, pady=(10, 0))
search_button.grid(row=0, column=1, padx=10, pady=(10, 0))

favorites_button.grid(row=0, column=0, padx=(5, 50), pady=(10, 0))

# Balloons (Tooltips)
searchTooltips = Pmw.Balloon(search_frame)
searchTooltips.bind(tv1, "Double-click a search result to see more detail")

root.mainloop()
