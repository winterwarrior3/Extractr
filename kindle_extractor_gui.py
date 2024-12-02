import tkinter as tk
from tkinter import filedialog, messagebox
import re
import os

def parse_clippings(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        content = file.read()
    
    # Split the content into individual clippings
    clippings = content.split('==========')
    
    books = {}
    
    for i, clipping in enumerate(clippings):
        clipping = clipping.strip()
        if not clipping:
            continue
        
        # Extract the book title and highlight
        lines = clipping.split('\n')
        
        if len(lines) < 3:
            continue
        
        title = lines[0].strip()
        highlight = lines[-1].strip()  # The last non-empty line should be the highlight
        
        # Remove potential Byte Order Mark (BOM) from the title
        title = title.lstrip('\ufeff')
        
        if title and highlight:
            if title not in books:
                books[title] = []
            books[title].append(highlight)
    
    return books

def write_to_markdown(books, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for title, highlights in books.items():
        # Create a valid filename
        file_name = re.sub(r'[\\/*?:"<>|]', "", title) + ".md"
        file_path = os.path.join(output_dir, file_name)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"# {title}\n\n")
            for highlight in highlights:
                file.write(f"- {highlight}\n\n")
    
    return output_dir

class KindleExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Kindle Highlights Extractor")
        
        # Set window size and position it in the center
        window_width = 500
        window_height = 250
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # Add padding around the window
        self.root.configure(padx=20, pady=20)
        
        # Create main frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(expand=True, fill='both')
        
        # Input file section
        self.input_frame = tk.LabelFrame(self.main_frame, text="Input File", padx=10, pady=10)
        self.input_frame.pack(fill='x', pady=(0, 10))
        
        self.input_label = tk.Label(self.input_frame, text="Select your 'My Clippings.txt' file:", wraplength=450)
        self.input_label.pack(side='left', padx=(0, 10))
        
        self.select_file_button = tk.Button(self.input_frame, text="Browse...", command=self.select_input_file)
        self.select_file_button.pack(side='right')
        
        # Output directory section
        self.output_frame = tk.LabelFrame(self.main_frame, text="Output Directory", padx=10, pady=10)
        self.output_frame.pack(fill='x', pady=(0, 10))
        
        self.output_label = tk.Label(self.output_frame, text="Select where to save the markdown files:", wraplength=450)
        self.output_label.pack(side='left', padx=(0, 10))
        
        self.select_dir_button = tk.Button(self.output_frame, text="Browse...", command=self.select_output_dir)
        self.select_dir_button.pack(side='right')
        
        # Process button
        self.process_button = tk.Button(self.main_frame, text="Convert Highlights", command=self.process_file, state='disabled')
        self.process_button.pack(pady=10)
        
        # Initialize variables
        self.input_file = None
        self.output_dir = None
        
    def select_input_file(self):
        file_path = filedialog.askopenfilename(
            title="Select My Clippings.txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.input_file = file_path
            self.input_label.config(text=f"Selected file: {os.path.basename(file_path)}")
            self.check_ready()
    
    def select_output_dir(self):
        dir_path = filedialog.askdirectory(title="Select Output Directory")
        if dir_path:
            self.output_dir = dir_path
            self.output_label.config(text=f"Selected directory: {dir_path}")
            self.check_ready()
    
    def check_ready(self):
        if self.input_file and self.output_dir:
            self.process_button.config(state='normal')
        else:
            self.process_button.config(state='disabled')

    def process_file(self):
        try:
            books = parse_clippings(self.input_file)
            if not books:
                messagebox.showerror("Error", "No highlights found in the selected file.")
                return
                
            output_dir = write_to_markdown(books, self.output_dir)
            messagebox.showinfo("Success", f"Highlights have been extracted!\nMarkdown files created in:\n{output_dir}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

def main():
    root = tk.Tk()
    app = KindleExtractorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
