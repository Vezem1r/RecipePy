from tkinter import *
from tkinter import ttk, messagebox, filedialog
import tkinter.scrolledtext as tkscrolled
from PIL import Image, ImageTk
import os
from ttkthemes import ThemedStyle

class RecipeRecord:
    def __init__(self, recipe_id, name, cooking_time, origin, description, ingredients=None, image_path=''):
        self.recipe_id = recipe_id
        self.name = name
        self.cooking_time = cooking_time
        self.origin = origin
        self.description = description
        self.ingredients = ingredients if ingredients else []
        self.image_path = image_path
        
    def is_valid(self):
        if not self.name or not self.cooking_time.isdigit() or not self.origin or not self.description:
            return False
        return True

class MainApp:
    def __init__(self):
        self.root = Tk()
        self.root.title("Recipe Database")
        self.root.resizable(width=False, height=False)
        self.app = Frame(self.root)
        self._initTreeView()
        self._initNotebookMenu()
        self._initMenu()
        self.selected_record = None
        self.records = []
        self.ingredients = [
        "Salt", "Pepper", "Sugar", "Flour", "Butter", "Eggs", "Milk",
        "Onion", "Garlic", "Tomato", "Basil", "Oregano", "Parsley", "Thyme",
        "Lemon", "Lime", "Chili", "Cinnamon", "Vanilla", "Honey",
        "Ginger", "Soy Sauce", "Vinegar", "Mustard", "Mayonnaise", "Paprika",
        "Cumin", "Coriander", "Sesame Seeds", "Coconut Milk", "Peanut Butter",
        "Cocoa Powder", "Maple Syrup", "Worcestershire Sauce", "Fish Sauce", "Tahini",
        "Red Wine", "White Wine", "Rice Vinegar", "Balsamic Vinegar", "Apple Cider Vinegar"
        ]
        self.app.pack(pady=25, padx=25)
        self.style = ThemedStyle(self.root)
        self.style.set_theme("breeze")
        self.image_path = None

    def _initTreeView(self):
        self.main_treeview = ttk.Treeview(self.app, columns=("id", "name", "cooking_time", "origin"), show='headings')
        self.main_treeview.heading("id", text="ID")
        self.main_treeview.heading("name", text="Name")
        self.main_treeview.heading("cooking_time", text="Cooking Time")
        self.main_treeview.heading("origin", text="Origin")

        for col in self.main_treeview['columns']:
            self.main_treeview.column(col, width=100)

        self.main_treeview.bind("<Double-1>", self.item_clicked)
        self.main_treeview.bind("<Button-3>", self.on_right_click)
        self.main_treeview.pack(side=RIGHT, fill=BOTH, padx=(0, 20))
        
        # Create a popup
        self.popup_menu = Menu(self.root, tearoff=0)
        self.popup_menu.add_command(label="Delete", command=self.delete_record)

    def on_right_click(self, event):
        row_id = self.main_treeview.identify_row(event.y)
        if row_id:
            self.main_treeview.selection_set(row_id)
            self.popup_menu.post(event.x_root, event.y_root) 

    def delete_record(self):
        selected_item = self.main_treeview.selection()
        if selected_item:
            record_id = self.main_treeview.item(selected_item)['values'][0]
            # Confirm deletion
            confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?")
            if confirm:
                # Remove the record from the list and refresh the Treeview
                self.records = [record for record in self.records if record.recipe_id != record_id]
                self._add_records()

    def item_clicked(self, event):
        selected_item = self.main_treeview.selection()
        if selected_item:
            # Get the record ID of the selected item
            record_id = self.main_treeview.item(selected_item)['values'][0]
            # Find the corresponding record by ID
            record = next((record for record in self.records if record.recipe_id == record_id), None)
            if record:
                self.show_details_window(record)

    def show_details_window(self, record):
        details_window = Toplevel(self.root)
        details_window.title(f"Details of {record.name}")
        details_window.geometry("600x405")
        
        details_window.lift()

        left_frame = Frame(details_window)
        left_frame.pack(side=LEFT, padx=(20, 10), pady=15)

        right_frame = Frame(details_window)
        right_frame.pack(side=RIGHT, padx=(10, 20), pady=15)

        # Editable fields
        Label(left_frame, text="Name:", font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=(0, 5))
        name_entry = Entry(left_frame, width=40)
        name_entry.grid(row=1, column=0, sticky='w', pady=(0, 10))
        name_entry.insert(0, record.name)

        Label(left_frame, text="Cooking Time:", font=('Arial', 10)).grid(row=2, column=0, sticky='w', pady=(0, 5))
        cooking_time_entry = Entry(left_frame, width=40)
        cooking_time_entry.grid(row=3, column=0, sticky='w', pady=(0, 10))
        cooking_time_entry.insert(0, record.cooking_time)

        Label(left_frame, text="Origin:", font=('Arial', 10)).grid(row=4, column=0, sticky='w', pady=(0, 5))
        origin_entry = Entry(left_frame, width=40)
        origin_entry.grid(row=5, column=0, sticky='w', pady=(0, 10))
        origin_entry.insert(0, record.origin)

        Label(left_frame, text="Description:", font=('Arial', 10)).grid(row=6, column=0, sticky='w', pady=(0, 5))
        description_text = tkscrolled.ScrolledText(left_frame, height=6, width=30)
        description_text.grid(row=7, column=0)
        description_text.insert(END, record.description)
        
        # Function to update image
        def update_image():
            new_image_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file", filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png"), ("all files", "*.*")))
            if new_image_path:
                record.image_path = new_image_path
                update_image_display(new_image_path)

        # Function to display image
        def update_image_display(image_path):
            try:
                image = Image.open(image_path)
                image = image.resize((250, 250), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                image_label.configure(image=photo)
                image_label.image = photo
                details_window.update_idletasks()
            except Exception as e:
                print(f"Error loading image: {e}")

        # Image display and update button
        image_label = Label(right_frame)
        image_label.pack(pady=(0, 10))
        if record.image_path and os.path.exists(record.image_path):
            update_image_display(record.image_path)

        change_image_button = Button(right_frame, text="Change Image", command=update_image)
        change_image_button.pack()

        def select_ingredients():
            ingredients_window = Toplevel(self.root)
            ingredients_window.title("Select Ingredients")

            num_columns = 3 

            def add_selected_ingredients():
                selected_ingredients = [self.ingredients[i] for i in range(len(self.ingredients)) if var_list[i].get() == 1]
                start_index = description_text.search("\nIngredients:", "1.0", END)
                if start_index:
            # deleting all symbols from ingredients start
                    description_text.delete(start_index, END) 
                description_text.insert(END, "\n\nIngredients:\n" + "\n".join(selected_ingredients))
                ingredients_window.destroy()

            for i, ingredient in enumerate(self.ingredients):
                row, column = divmod(i, num_columns)  # Определение строки и столбца для ингредиента
                chk = Checkbutton(ingredients_window, text=ingredient, variable=var_list[i])
                chk.grid(row=row, column=column, sticky=W)  # Размещение ингредиентов в сетке

            # "Add"
            add_button = Button(ingredients_window, text="Add", command=add_selected_ingredients, width=10)
            add_button.grid(row=row + 1, column=0, columnspan=num_columns, pady=10)

            # "Exit"
            close_button = Button(ingredients_window, text="Exit", command=ingredients_window.destroy, width=10)
            close_button.grid(row=row + 2, column=0, columnspan=num_columns, pady=10)

        # save flags status
        var_list = [IntVar() for _ in range(len(self.ingredients))]

        ingredients_button = Button(left_frame, text="Add Ingredients", command=select_ingredients)
        ingredients_button.grid(row=8, column=0, pady=(10, 0))

        # Save Changes Button
        def save_changes():
            record.name = name_entry.get()
            record.cooking_time = cooking_time_entry.get()
            record.origin = origin_entry.get()
            record.description = description_text.get("1.0", "end-1c")
            self._add_records()
            details_window.destroy()
            messagebox.showinfo("Update Successful", "The recipe data has been updated successfully.")

        save_button = Button(left_frame, text="Save Changes", command=save_changes)
        save_button.grid(row=9, column=0, columnspan=2, pady=(10, 0))

    def _initNotebookMenu(self):
        self.notebook = ttk.Notebook(self.app)
        self.notebook.pack(side=RIGHT, fill=BOTH, padx=(20, 0))
        self._initInsertForm()

    def _initInsertForm(self):
        self.new_record_notebook_tab = ttk.Frame(self.notebook, height=400, width=300)
        self.notebook.add(self.new_record_notebook_tab, text="New Recipe")
        #self.notebook.add(self.new_record_notebook_tab, text=" " * 11 +"New Recipe" + " " * 11)
        self.new_record_form = ttk.Frame(self.new_record_notebook_tab)
        self._createFormField("Name", 0)
        self._createFormField("Cooking Time in min", 2)
        self._createFormField("Origin", 4)
        self.description_label = ttk.Label(self.new_record_form, text="Description")
        self.description_text = Text(self.new_record_form, width=40, height=4)
        self.description_label.grid(row=6, pady=(15, 0), sticky=W)
        self.description_text.grid(row=7, sticky=NSEW, pady=(0, 10))
        self.add_image_button = ttk.Button(self.new_record_form, text="Add Image", command=self.add_image)
        self.add_image_button.grid(row=8, column=0, pady=(10, 10), padx=(0, 5), sticky='e')
        self.add_record_button = ttk.Button(self.new_record_form, text="Add Recipe", command=self.add_record)
        self.add_record_button.grid(row=8, column=0, pady=(10, 10), padx=(5, 0), sticky='w')
        self.new_record_form.pack(fill=BOTH, padx=25, pady=10)

        self.new_ingredient_notebook_tab = ttk.Frame(self.notebook, height=400, width=300)
        self.notebook.add(self.new_ingredient_notebook_tab, text="New Ingredient")
        #self.notebook.add(self.new_ingredient_notebook_tab, text=" " * 11 +"New Ingredient" + " " * 11)
        self.new_ingredient_form = ttk.Frame(self.new_ingredient_notebook_tab)
        self._createIngredientField("Ingredient Name", 0)
        self.add_ingredient_button = ttk.Button(self.new_ingredient_form, text="Add Ingredient", command=self.add_ingredient)
        self.add_ingredient_button.grid(row=2, column=0, pady=(10, 10))
        self.new_ingredient_form.pack(fill=BOTH, padx=25, pady=10)

    def _createIngredientField(self, label, row):
        label_widget = ttk.Label(self.new_ingredient_form, text=label)
        entry_widget = ttk.Entry(self.new_ingredient_form, width=40)
        label_widget.grid(row=row, pady=(15, 0), sticky=W)
        entry_widget.grid(row=row+1, sticky=NSEW)
        self.new_ingredient_form.columnconfigure(0, weight=1)
        
    def add_ingredient(self):
        ingredient_name = self.new_ingredient_form.winfo_children()[1].get()
        if ingredient_name:
            messagebox.showinfo("Ingredient Added", f"The ingredient '{ingredient_name}' has been added successfully.")
            self.ingredients.append(ingredient_name)
            self.new_ingredient_form.winfo_children()[1].delete(0, END)  # Clear the entry field after adding the ingredient
        else:
            messagebox.showerror("Empty Field", "Please enter the name of the ingredient.")

    def _createFormField(self, label, row):
        label_widget = ttk.Label(self.new_record_form, text=label)
        entry_widget = ttk.Entry(self.new_record_form, width=40)
        label_widget.grid(row=row, pady=(15, 0), sticky=W)
        entry_widget.grid(row=row+1, sticky=NSEW)

    def _initMenu(self):
        self.top_menu_bar = Menu(self.root)
        self.settings_menu = Menu(self.top_menu_bar, tearoff=0)

        self.settings_menu.add_command(label="Configuration", command=self.open_config_window)  # Add Configuration option
        self.settings_menu.add_command(label="Quit", command=self.root.quit)

        self.top_menu_bar.add_cascade(label="Settings", menu=self.settings_menu)
        self.root.config(menu=self.top_menu_bar)
        
        file_menu = Menu(self.top_menu_bar, tearoff=0)
        file_menu.add_command(label="New")
        file_menu.add_command(label="Open")
        file_menu.add_separator()
        file_menu.add_command(label="Save")
        file_menu.add_command(label="Save As")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        edit_menu = Menu(self.top_menu_bar, tearoff=0)
        edit_menu.add_command(label="Copy", command=self.copy_record)
        edit_menu.add_command(label="Paste", command=self.paste_record)
        edit_menu.add_separator()
        edit_menu.add_command(label="Delete All", command=self.delete_all_items)
        
        selection_menu = Menu(self.top_menu_bar, tearoff=0)
        selection_menu.add_command(label="Select All", command=self.select_all_records)
        selection_menu.add_command(label="Deselect All", command=self.deselect_all_records)
        
        self.top_menu_bar.add_cascade(label="File", menu=file_menu)
        self.top_menu_bar.add_cascade(label="Edit", menu=edit_menu)
        self.top_menu_bar.add_cascade(label="Selection", menu=selection_menu)
        
    def delete_all_items(self):
        confirm = messagebox.askyesno("Confirm Delete All", "Are you sure you want to delete all records?")
        if confirm:
            self.records = []
            self._add_records()    
            
    def select_all_records(self):
        for item in self.main_treeview.get_children():
            self.main_treeview.selection_add(item)

    def deselect_all_records(self):
        for item in self.main_treeview.selection():
            self.main_treeview.selection_remove(item)
            
    def copy_record(self):
        selected_items = self.main_treeview.selection()
        if selected_items:
            self.selected_records = []
            for item in selected_items:
                record_id = self.main_treeview.item(item)['values'][0]
                record = next((record for record in self.records if record.recipe_id == record_id), None)
                if record:
                    self.selected_records.append(record)

    def paste_record(self):
        if self.selected_records:
            for selected_record in self.selected_records:
                new_record = RecipeRecord(
                    recipe_id=len(self.records) + 1,
                    name=selected_record.name,
                    cooking_time=selected_record.cooking_time,
                    origin=selected_record.origin,
                    description=selected_record.description,
                    image_path=selected_record.image_path
                )
                self.records.append(new_record)
            self._add_records()
            self.selected_records = []

    def open_config_window(self):
        config_window = Toplevel(self.root)
        config_window.title("Configuration")
        config_window.geometry("400x300")

        tab_control = ttk.Notebook(config_window)

        settings_tab = ttk.Frame(tab_control)
        about_us_tab = ttk.Frame(tab_control)

        tab_control.add(settings_tab, text='Settings')
        tab_control.add(about_us_tab, text='About Us')
        about_us_label = Label(about_us_tab, text="About Us Placeholder\nProject for URO\nVersion: 1.0.0\nAuthor: AKU0003\nVŠB-TUO", padx=5, pady=5)
        about_us_label.grid(column=0, row=0, sticky='nw', padx=130)

        license_button = Button(about_us_tab, text="License Agreement", command=self.open_license_window)
        license_button.grid(column=0, row=1, pady=10, sticky='nw',padx=138)

        tab_control.pack(expand=1, fill="both")
        theme_label = Label(settings_tab, text="Select Theme:", padx=5, pady=5)
        theme_label.grid(column=0, row=0, sticky='W')
        available_themes = self.style.theme_names()
        self.theme_combobox = ttk.Combobox(settings_tab, values=available_themes, state="readonly", width=21)
        self.theme_combobox.grid(column=1, row=0, sticky='W', padx=5, pady=5)
        self.theme_combobox.bind("<<ComboboxSelected>>", self.change_theme)

        # Import File section
        import_file_label = Label(settings_tab, text="Import File:", padx=5, pady=5)
        import_file_label.grid(column=0, row=2, sticky='W')
        import_file_button = Button(settings_tab, text="Import", width=20)
        import_file_button.grid(column=1, row=2, sticky='W', padx=5, pady=5)

        # Export File section
        export_file_label = Label(settings_tab, text="Export File:", padx=5, pady=5)
        export_file_label.grid(column=0, row=3, sticky='W')
        export_file_button = Button(settings_tab, text="Export", width=20)
        export_file_button.grid(column=1, row=3, sticky='W', padx=5, pady=5)

        # Import Ingredients section
        import_ingredients_label = Label(settings_tab, text="Import Ingredients:", padx=5, pady=5)
        import_ingredients_label.grid(column=0, row=4, sticky='W')
        import_ingredients_button = Button(settings_tab, text="Import Ingredients", width=20)
        import_ingredients_button.grid(column=1, row=4, sticky='W', padx=5, pady=5)

        tab_control.pack(expand=1, fill="both")

    def change_theme(self, event):
        selected_theme = self.theme_combobox.get()
        self.style.set_theme(selected_theme)

    def open_license_window(self):
        license_window = Toplevel(self.root)
        license_window.title("License Agreement")
        license_window.geometry("500x400")

        license_text = """- Jak můžete přerušit rozhovor dvou hluchoněmých?\n- Vypnout světla"""

        # Display the license text in a label or a non-editable text widget
        license_label = Label(license_window, text=license_text, justify=LEFT, anchor="nw")
        license_label.pack(padx=10, pady=10)

    def add_record(self):
        recipe_id = 1 if len(self.main_treeview.get_children()) == 0 else int(self.main_treeview.item(self.main_treeview.get_children()[-1])['values'][0]) + 1
        name = self.new_record_form.winfo_children()[1].get()
        cooking_time = self.new_record_form.winfo_children()[3].get()
        origin = self.new_record_form.winfo_children()[5].get()
        description = self.description_text.get("1.0", "end-1c")
        new_image_path = self.image_path

        if not origin:
            origin = "None"
        new_record = RecipeRecord(recipe_id, name, cooking_time, origin, description,image_path=new_image_path)
        if not new_record.is_valid():
            messagebox.showerror("Invalid Record", "Please check the input values.")
            return

        self.records.append(new_record)
        self._add_records()
        for entry in self.new_record_form.winfo_children():
            if isinstance(entry, ttk.Entry):
                entry.delete(0, END)
        self.description_text.delete("1.0", END)
        self.add_image_button.config(text='Add image')
        
        self.image_path = None

    def _add_records(self):
        for i in self.main_treeview.get_children():
            self.main_treeview.delete(i)
        for record in self.records:
            self.main_treeview.insert("", "end", values=(record.recipe_id, record.name, record.cooking_time, record.origin))

    def add_image(self):
        self.image_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file", filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        self.add_image_button.config(text='Image picked')
        
    def run(self):
        self.root.mainloop()
app = MainApp()
app.run()
