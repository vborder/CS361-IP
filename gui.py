import tkinter
from tkinter import *
from tkinter import ttk
import z_scraper
import webbrowser
import pandas as pd

favorites = []

root = tkinter.Tk()
root.title("Padmapper")
root.geometry("800x400")
root.resizable(0, 0)

# define fonts and colors
search_color = "#f58509"
favorites_color = "#e90c57"
delete_color ="#d92222"
input_color = "#"
large_font = ("SimSun", 14)
small_font = ("SimSun", 10)


# define functions
def search():
    val = search_entry.get()
    scrape = z_scraper.ZScraper()
    data = scrape.run(val)
    load_data(data)


def save_favorites():
    favorites.append(tv1.set(tv1.focus()))
    popup_msg("The listing was saved")


def popup_msg(msg):
    popup = tkinter.Tk()
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
    my_favorites_frame = tkinter.LabelFrame(favorites_window, width=1200, height=225, bg="white")
    my_favorites_frame.pack(pady=30)
    my_favorites_frame.pack_propagate(0)

    fv1 = ttk.Treeview(my_favorites_frame)
    fv1.place(relheight=1, relwidth=1)

    favesscrolly = tkinter.Scrollbar(my_favorites_frame, orient="vertical", command=fv1.yview)
    favesscrollx = tkinter.Scrollbar(my_favorites_frame, orient="horizontal", command=fv1.xview)
    fv1.configure(xscrollcommand=favesscrollx.set, yscrollcommand=favesscrolly.set)
    favesscrollx.pack(side="bottom", fill="x")
    favesscrolly.pack(side="right", fill="y")

    # load favorites
    df = pd.DataFrame(favorites)
    fv1["column"] = tv1["columns"]
    fv1["show"] = "headings"

    for column in fv1["columns"]:
        fv1.heading(column, text=column)

    df_rows = df.to_numpy().tolist()
    for row in df_rows:
        fv1.insert("", "end", values=row)

    fv1.bind("<Double-1>", favOnDoubleClick)


def onDoubleClick(event):
    cur_item = tv1.item(tv1.focus())
    item = tv1.identify('item', event.x, event.y)

    # popup window
    listing_window = Toplevel(root, bg="white")
    listing_window.title("Listing detail")
    listing_window.geometry("600x400")
    listing_window_frame = tkinter.Frame(listing_window, bg="white", height=100)
    listing_window_frame.pack(fill=X, expand=False)

    # listing_window_bg = tkinter.Frame(listing_window, bg="white")
    Label(listing_window_frame, text=cur_item['values'][0], bg="white").pack(pady=10, side=TOP, anchor='w')
    Label(listing_window_frame, text="square footage: " + cur_item['values'][1], bg="white").pack(pady=2, side=TOP,
                                                                                                  anchor='w')
    Label(listing_window_frame, text="price: " + cur_item['values'][2], bg="white").pack(pady=2, side=TOP, anchor='w')

    # url link in window
    link = Label(listing_window, text=cur_item['values'][3], bg="white", cursor="hand2")
    link.pack(pady=2, side=TOP, anchor='w')
    link.bind("<Button-1>", lambda e: callback(cur_item['values'][3]))

    # button here to save listing to favorites
    save_to_favorites_button = tkinter.Button(listing_window_frame, text="Save", font=small_font, bg=favorites_color,
                                              fg="white", command=save_favorites)
    save_to_favorites_button.pack(side=TOP, padx=5, pady=10, anchor='e')


def favOnDoubleClick(event):
    cur_item = tv1.item(tv1.focus())
    item = tv1.identify('item', event.x, event.y)

    # popup window
    listing_window = Toplevel(root, bg="white")
    listing_window.title("Listing detail")
    listing_window.geometry("600x400")
    listing_window_frame = tkinter.Frame(listing_window, bg="white", height=100)
    listing_window_frame.pack(fill=X, expand=False)

    # listing_window_bg = tkinter.Frame(listing_window, bg="white")
    Label(listing_window_frame, text=cur_item['values'][0], bg="white").pack(pady=10, side=TOP, anchor='w')
    Label(listing_window_frame, text="square footage: " + cur_item['values'][1], bg="white").pack(pady=2, side=TOP,
                                                                                                  anchor='w')
    Label(listing_window_frame, text="price: " + cur_item['values'][2], bg="white").pack(pady=2, side=TOP, anchor='w')

    # url link in window
    link = Label(listing_window, text=cur_item['values'][3], bg="white", cursor="hand2")
    link.pack(pady=2, side=TOP, anchor='w')
    link.bind("<Button-1>", lambda e: callback(cur_item['values'][3]))

    delete_favorite_button = tkinter.Button(listing_window_frame, text="Delete", font=small_font, bg=delete_color,
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

    for column in tv1["columns"]:
        tv1.heading(column, text=column)

    data_rows = data.to_numpy().tolist()
    for row in data_rows:
        tv1.insert("", "end", values=row)

    # event binding added
    tv1.bind("<Double-1>", onDoubleClick)


def clear_data():
    tv1.delete(*tv1.get_children())


# create frames
search_frame = tkinter.Frame(root, bg="white", height=100)
search_frame.pack(fill=X, expand=False)

output_bg = tkinter.Frame(root, bg="white")
output_frame = tkinter.LabelFrame(output_bg, text="Search results", width=1200, height=225)

input_frame = tkinter.LabelFrame(search_frame, text="Enter the zip code to search", bg=search_color, fg="white",
                                 width=100)
favorites_frame = tkinter.LabelFrame(search_frame, text="My favorites", bg=favorites_color, fg="white", width=150,
                                     height=40)

output_frame.pack(pady=30)
output_frame.pack_propagate(0)
output_bg.pack(fill=BOTH, expand=True)
input_frame.pack(pady=10, padx=10, side=LEFT)
favorites_frame.pack(pady=10, padx=10, side=RIGHT, anchor='ne')

# Search Treeview
tv1 = ttk.Treeview(output_frame)
tv1.place(relheight=1, relwidth=1)

treescrolly = tkinter.Scrollbar(output_frame, orient="vertical", command=tv1.yview)
treescrollx = tkinter.Scrollbar(output_frame, orient="horizontal", command=tv1.xview)
tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)
treescrollx.pack(side="bottom", fill="x")
treescrolly.pack(side="right", fill="y")

# Faves Treeview
favorites_window = Toplevel(root, bg="white")
favorites_window.title("My favorites")
favorites_window.geometry("600x400")
my_favorites_frame = tkinter.LabelFrame(favorites_window, width=1200, height=225, bg="white")
my_favorites_frame.pack(pady=30)
my_favorites_frame.pack_propagate(0)

fv1 = ttk.Treeview(my_favorites_frame)
fv1.place(relheight=1, relwidth=1)

favesscrolly = tkinter.Scrollbar(my_favorites_frame, orient="vertical", command=fv1.yview)
favesscrollx = tkinter.Scrollbar(my_favorites_frame, orient="horizontal", command=fv1.xview)
fv1.configure(xscrollcommand=favesscrollx.set, yscrollcommand=favesscrolly.set)
favesscrollx.pack(side="bottom", fill="x")
favesscrolly.pack(side="right", fill="y")

# input frame layout
search_entry = tkinter.Entry(input_frame, width=20, font=small_font)
search_button = tkinter.Button(input_frame, text="Search", font=small_font, bg=search_color, fg="white", command=search)
favorites_button = tkinter.Button(favorites_frame, text="View", font=small_font, bg=favorites_color, fg="white",
                                  command=favorites_list)

# output frame layout
# table = pd.Table(output_frame, dataframe=data)
# table.show()

# implement city search?
# search_method = IntVar()
# search_method.set(1)
# search_city = tkinter.Radiobutton(input_frame, text="Search city", variable=search_method, value=1)
# search_zip = tkinter.Radiobutton(input_frame, text="Search zip code", variable=search_method, value=2)

search_entry.grid(row=0, column=0, padx=10, pady=(10, 0))
search_button.grid(row=0, column=1, padx=10, pady=(10, 0))

favorites_button.grid(row=0, column=0, padx=(5, 50), pady=(10, 0))

root.mainloop()
