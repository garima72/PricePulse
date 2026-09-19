import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def search_products():
    product = product_entry.get()

    try:
        min_price = int(min_price_entry.get())
        max_price = int(max_price_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Enter valid prices")
        return

    if product == "":
        messagebox.showerror("Error", "Enter product name")
        return

    options = Options()

    options.add_argument("--start-maximized")  # for maximizing the window

    driver = webdriver.Chrome(options=options)

    driver.get("https://www.amazon.in/")

    time.sleep(3)

    search = driver.find_element(
        By.ID, "twotabsearchtextbox"
    )  # for tapping on search box

    search.send_keys(product)
    search.send_keys(Keys.ENTER)

    time.sleep(5)

    products = driver.find_elements(
        By.CSS_SELECTOR,
        "div[data-component-type='s-search-result']"  # for selecting elements
    )

    results_text.delete("1.0", tk.END)

    results_text.insert(
        tk.END,
        "Products within your price range:\n\n"
    )

    count = 0

    for product_item in products:
        if count == 5: # first five search results in the range will extracted
         break
        try:
            name = product_item.find_element(  # extracting text of product
                By.CSS_SELECTOR, "h2"
            ).text

            price_text = product_item.find_element(  # extracting price
                By.CSS_SELECTOR, ".a-price-whole"
            ).text

            price = int(price_text.replace(",", ""))  # remove commas

            if min_price <= price <= max_price:

                results_text.insert(
                    tk.END,
                    f"Product: {name}\n"
                )

                results_text.insert(
                    tk.END,
                    f"Price: ₹{price}\n"
                )

                results_text.insert(
                    tk.END,
                    "-" * 40 + "\n"
                )

                count += 1

        except:
            continue

    if count == 0:
        results_text.insert(
            tk.END,
            "No products found in your price range."
        )

    driver.quit()


# Create GUI window
window = tk.Tk()
window.title("PricePulse - Price Tracker")
window.state("zoomed")

# Heading
heading = tk.Label(
    window,
    text="PRICEPULSE",
    font=("Arial", 20, "bold")
)
heading.pack(pady=10)

subtitle = tk.Label(
    window,
    text="Price Tracker",
    font=("Arial", 12)
)

subtitle.pack()

# Product Name
tk.Label(
    window,
    text="Product Name:"
).pack(pady=(20, 5))

product_entry = tk.Entry(
    window,
    width=40
)
product_entry.pack()
# Minimum Price
tk.Label(
    window,
    text="Minimum Price:"
).pack(pady=(10, 5))
min_price_entry = tk.Entry(
    window,
    width=40
)
min_price_entry.pack()

# Maximum Price
tk.Label(
    window,
    text="Maximum Price:"
).pack(pady=(10, 5))

max_price_entry = tk.Entry(
    window,
    width=40
)

max_price_entry.pack()

# Search Button
search_button = tk.Button(
    window,
    text="SEARCH PRODUCTS",
    command=search_products
)

search_button.pack(pady=20)

# Results Heading
tk.Label(
    window,
    text="Results:",
    font=("Arial", 12, "bold")
).pack()

# Results Text Box
results_text = tk.Text(
    window,
    width=80,
    height=20
)
results_text.pack(pady=10)

# Run GUI
window.mainloop()