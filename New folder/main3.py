import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
import os
from typing import List, Dict, Union


class Book:
    def __init__(self, title: str, author: str, genre: str, year: int):
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year

    def to_dict(self) :
        """Convert book data to dictionary for serialization"""
        return {
            'title': self.title,
            'author': self.author,
            'genre': self.genre,
            'year': self.year
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Union[str, int]]):
        """Create Book instance from dictionary"""
        return cls(data['title'], data['author'], data['genre'], data['year'])

class Library:
    def __init__(self):
        self.books: List[Book] = []
        self.json_filename = "library_data.json"
        self.csv_filename = "library_data.csv"
        self.load_library()  # Load data on initialization

    def add_book(self, book: Book) -> None:
        """Add a book to the library"""
        self.books.append(book)
        self.save_library()

    def remove_book(self, title: str) -> bool:
        """Remove a book by title"""
        for i, book in enumerate(self.books):
            if book.title.lower() == title.lower():
                del self.books[i]
                self.save_library()
                return True
        return False

    def search_books(self, query: str) -> List[Book]:
        """Search books by title, author, or genre"""
        results = []
        query = query.lower()
        for book in self.books:
            if (query in book.title.lower() or
                    query in book.author.lower() or
                    query in book.genre.lower()):
                results.append(book)
        return results

    def get_all_books(self) -> List[Book]:
        """Get all books in the library"""
        return self.books

    def save_library(self, format: str = 'json') -> bool:
        """Save library to file (default: JSON)"""
        try:
            if format == 'json':
                return self._save_to_json()
            elif format == 'csv':
                return self._save_to_csv()
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save library: {str(e)}")
            return False

    def _save_to_json(self) -> bool:
        """Internal method to save to JSON file"""
        try:
            with open(self.json_filename, 'w') as f:
                json.dump([book.to_dict() for book in self.books], f, indent=2)
            return True
        except Exception as e:
            raise Exception(f"JSON save error: {str(e)}")

    def _save_to_csv(self) -> bool:
        """Internal method to save to CSV file"""
        try:
            with open(self.csv_filename, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['title', 'author', 'genre', 'year'])
                writer.writeheader()
                for book in self.books:
                    writer.writerow(book.to_dict())
            return True
        except Exception as e:
            raise Exception(f"CSV save error: {str(e)}")

    def load_library(self) -> bool:
        """Load library from available files (JSON preferred)"""
        try:
            if os.path.exists(self.json_filename):
                return self._load_from_json()
            elif os.path.exists(self.csv_filename):
                return self._load_from_csv()
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load library: {str(e)}")
            return False

    def _load_from_json(self) -> bool:
        """Internal method to load from JSON file"""
        try:
            with open(self.json_filename, 'r') as f:
                data = json.load(f)
                self.books = [Book.from_dict(book_data) for book_data in data]
            return True
        except Exception as e:
            raise Exception(f"JSON load error: {str(e)}")

    def _load_from_csv(self) -> bool:
        """Internal method to load from CSV file"""
        try:
            with open(self.csv_filename, 'r', newline='') as f:
                reader = csv.DictReader(f)
                self.books = [Book(row['title'], row['author'], row['genre'], int(row['year']))
                              for row in reader]
            return True
        except Exception as e:
            raise Exception(f"CSV load error: {str(e)}")

    def export_library(self, filename: str, format: str = 'json') -> bool:
        """Export library to specified file"""
        try:
            if format == 'json':
                with open(filename, 'w') as f:
                    json.dump([book.to_dict() for book in self.books], f, indent=2)
                return True
            elif format == 'csv':
                with open(filename, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=['title', 'author', 'genre', 'year'])
                    writer.writeheader()
                    for book in self.books:
                        writer.writerow(book.to_dict())
                return True
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export library: {str(e)}")
            return False

    def import_library(self, filename: str) -> bool:
        """Import library from specified file"""
        try:
            temp_books = []
            if filename.endswith('.json'):
                with open(filename, 'r') as f:
                    data = json.load(f)
                    temp_books = [Book.from_dict(book_data) for book_data in data]
            elif filename.endswith('.csv'):
                with open(filename, 'r', newline='') as f:
                    reader = csv.DictReader(f)
                    temp_books = [Book(row['title'], row['author'], row['genre'], int(row['year']))
                                  for row in reader]
            else:
                messagebox.showerror("Error", "Unsupported file format")
                return False

            self.books.extend(temp_books)
            self.save_library()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import library: {str(e)}")
            return False


class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.library = Library()

        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()

        self.setup_ui()
        self.update_book_list()

    def configure_styles(self):
        """Configure the visual styles for the application"""
        # Color scheme
        self.bg_color = '#f5f5f5'
        self.primary_color = '#3498db'
        self.secondary_color = '#2980b9'
        self.accent_color = '#e74c3c'
        self.success_color = '#2ecc71'
        self.text_color = '#2c3e50'
        self.header_color = '#2c3e50'

        # Configure styles
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', background=self.bg_color, foreground=self.text_color)
        self.style.configure('TButton',
                             background=self.primary_color,
                             foreground='white',
                             font=('Helvetica', 10),
                             padding=5)
        self.style.map('TButton',
                       background=[('active', self.secondary_color), ('pressed', self.secondary_color)],
                       foreground=[('active', 'white'), ('pressed', 'white')])

        self.style.configure('Header.TLabel',
                             font=('Helvetica', 14, 'bold'),
                             foreground=self.header_color)

        self.style.configure('Treeview',
                             font=('Helvetica', 10),
                             rowheight=25,
                             background='white',
                             fieldbackground='white')
        self.style.configure('Treeview.Heading',
                             font=('Helvetica', 10, 'bold'),
                             background=self.primary_color,
                             foreground='white')

        self.style.configure('Accent.TButton',
                             background=self.accent_color)
        self.style.map('Accent.TButton',
                       background=[('active', '#c0392b'), ('pressed', '#c0392b')])

        self.style.configure('Success.TButton',
                             background=self.success_color)
        self.style.map('Success.TButton',
                       background=[('active', '#27ae60'), ('pressed', '#27ae60')])

        self.style.configure('TLabelFrame',
                             background=self.bg_color,
                             relief=tk.GROOVE,
                             borderwidth=2)
        self.style.configure('TLabelFrame.Label',
                             background=self.bg_color,
                             foreground=self.text_color)

    def setup_ui(self):
        """Set up the user interface"""
        self.root.title("Personal Library Management System")
        self.root.geometry("1100x700")
        self.root.configure(bg=self.bg_color)

        # Header Frame
        self.header_frame = ttk.Frame(self.root, style='TFrame')
        self.header_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(self.header_frame,
                  text="Personal Library Management System",
                  style='Header.TLabel').pack(side=tk.LEFT)

        # Main Container Frame
        self.main_container = ttk.Frame(self.root, style='TFrame')
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Left Frame - Book List (70% width)
        self.list_frame = ttk.LabelFrame(self.main_container,
                                         text=" Book Collection ",
                                         padding=10)
        self.list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Right Frame - Controls (30% width)
        self.control_frame = ttk.Frame(self.main_container, style='TFrame', width=350)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

        # Book list treeview
        self.tree = ttk.Treeview(self.list_frame,
                                 columns=('Title', 'Author', 'Genre', 'Year'),
                                 show='headings',
                                 selectmode='browse')
        self.tree.heading('Title', text='Title', anchor=tk.W)
        self.tree.heading('Author', text='Author', anchor=tk.W)
        self.tree.heading('Genre', text='Genre', anchor=tk.W)
        self.tree.heading('Year', text='Year', anchor=tk.W)
        self.tree.column('Title', width=250, anchor=tk.W)
        self.tree.column('Author', width=200, anchor=tk.W)
        self.tree.column('Genre', width=150, anchor=tk.W)
        self.tree.column('Year', width=80, anchor=tk.W)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Search Section
        self.search_frame = ttk.LabelFrame(self.control_frame,
                                           text=" Search Books ",
                                           padding=10)
        self.search_frame.pack(fill=tk.X, padx=5, pady=5)

        self.search_entry = ttk.Entry(self.search_frame, font=('Helvetica', 10))
        self.search_entry.pack(fill=tk.X, padx=5, pady=(0, 5))

        self.search_button = ttk.Button(self.search_frame,
                                        text="Search",
                                        command=self.search_books)
        self.search_button.pack(fill=tk.X, padx=5, pady=2)

        self.show_all_button = ttk.Button(self.search_frame,
                                          text="Show All",
                                          command=self.update_book_list)
        self.show_all_button.pack(fill=tk.X, padx=5, pady=2)

        # Add Book Section
        self.add_frame = ttk.LabelFrame(self.control_frame,
                                        text=" Add New Book ",
                                        padding=10)
        self.add_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(self.add_frame, text="Title:").pack(anchor=tk.W, pady=(0, 2))
        self.title_entry = ttk.Entry(self.add_frame, font=('Helvetica', 10))
        self.title_entry.pack(fill=tk.X, padx=5, pady=(0, 5))

        ttk.Label(self.add_frame, text="Author:").pack(anchor=tk.W, pady=(0, 2))
        self.author_entry = ttk.Entry(self.add_frame, font=('Helvetica', 10))
        self.author_entry.pack(fill=tk.X, padx=5, pady=(0, 5))

        ttk.Label(self.add_frame, text="Genre:").pack(anchor=tk.W, pady=(0, 2))
        self.genre_entry = ttk.Entry(self.add_frame, font=('Helvetica', 10))
        self.genre_entry.pack(fill=tk.X, padx=5, pady=(0, 5))

        ttk.Label(self.add_frame, text="Year:").pack(anchor=tk.W, pady=(0, 2))
        self.year_entry = ttk.Entry(self.add_frame, font=('Helvetica', 10))
        self.year_entry.pack(fill=tk.X, padx=5, pady=(0, 5))

        self.add_button = ttk.Button(self.add_frame,
                                     text="Add Book",
                                     style='Success.TButton',
                                     command=self.add_book)
        self.add_button.pack(fill=tk.X, padx=5, pady=5)

        # Remove Book Section
        self.remove_frame = ttk.LabelFrame(self.control_frame,
                                           text=" Remove Book ",
                                           padding=10)
        self.remove_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(self.remove_frame, text="Title to remove:").pack(anchor=tk.W, pady=(0, 2))
        self.remove_entry = ttk.Entry(self.remove_frame, font=('Helvetica', 10))
        self.remove_entry.pack(fill=tk.X, padx=5, pady=(0, 5))

        self.remove_button = ttk.Button(self.remove_frame,
                                        text="Remove Book",
                                        style='Accent.TButton',
                                        command=self.remove_book)
        self.remove_button.pack(fill=tk.X, padx=5, pady=5)

        # Import/Export Section
        self.io_frame = ttk.LabelFrame(self.control_frame,
                                       text=" Import/Export ",
                                       padding=10)
        self.io_frame.pack(fill=tk.X, padx=5, pady=5)

        self.export_button = ttk.Button(self.io_frame,
                                        text="Export Library",
                                        command=self.export_library)
        self.export_button.pack(fill=tk.X, padx=5, pady=2)

        self.import_button = ttk.Button(self.io_frame,
                                        text="Import Library",
                                        command=self.import_library)
        self.import_button.pack(fill=tk.X, padx=5, pady=2)

        # Status Bar
        self.status_frame = ttk.Frame(self.root, style='TFrame', height=25)
        self.status_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.status_label = ttk.Label(self.status_frame,
                                      text="Ready",
                                      style='TLabel',
                                      anchor=tk.W)
        self.status_label.pack(fill=tk.X, padx=5)

    def update_book_list(self, books: List[Book] = None) -> None:
        """Update the book list display"""
        self.tree.delete(*self.tree.get_children())
        books_to_show = books if books is not None else self.library.get_all_books()
        for book in books_to_show:
            self.tree.insert('', tk.END, values=(book.title, book.author, book.genre, book.year))

        count = len(books_to_show)
        total = len(self.library.books)
        if books is not None:
            self.status_label.config(text=f"Showing {count} of {total} books (filtered)")
        else:
            self.status_label.config(text=f"Showing all {count} books")

    def search_books(self) -> None:
        """Search books based on user query"""
        query = self.search_entry.get()
        if query:
            results = self.library.search_books(query)
            self.update_book_list(results)

    def add_book(self) -> None:
        """Add a new book to the library"""
        title = self.title_entry.get()
        author = self.author_entry.get()
        genre = self.genre_entry.get()
        year = self.year_entry.get()

        if not all([title, author, genre, year]):
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            year = int(year)
            if year < 0 or year > 2100:
                raise ValueError("Year must be between 0 and 2100")
        except ValueError:
            messagebox.showerror("Error", "Year must be a valid number!")
            return

        book = Book(title, author, genre, year)
        self.library.add_book(book)
        self.update_book_list()

        # Clear the form
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)

        messagebox.showinfo("Success", "Book added successfully!")

    def remove_book(self) -> None:
        """Remove a book from the library"""
        title = self.remove_entry.get()
        if not title:
            messagebox.showerror("Error", "Please enter a title to remove!")
            return

        if self.library.remove_book(title):
            self.update_book_list()
            self.remove_entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Book removed successfully!")
        else:
            messagebox.showerror("Error", "Book not found!")

    def export_library(self) -> None:
        """Export the library to a file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Library"
        )
        if file_path:
            format = 'json' if file_path.endswith('.json') else 'csv'
            if self.library.export_library(file_path, format):
                messagebox.showinfo("Success", "Library exported successfully!")

    def import_library(self) -> None:
        """Import books from a file"""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("CSV files", "*.csv"), ("All files", "*.*")],
            title="Import Library"
        )
        if file_path:
            if self.library.import_library(file_path):
                self.update_book_list()
                messagebox.showinfo("Success", "Library imported successfully!")


def main():
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()