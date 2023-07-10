import glob
import os.path
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import shutil
import os
import gpt_funs
import preprocess
from PIL import Image, ImageTk
import PyPDF2
import customtkinter
from tkinter import scrolledtext

# -------------------------- DEFINING GLOBAL VARIABLES -------------------------
import root
selectionbar_color = '#eff5f6'
sidebar_color = '#F5E1FD'
header_color = sidebar_color
visualisation_frame_color = "#ffffff"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


# ------------------------------- ROOT WINDOW ----------------------------------


class TkinterApp(tk.Tk):
    """
     The class creates a header and sidebar for the application. Also creates
     two submenus in the sidebar, one for attendance overview with options to
     track students and modules, view poor attendance and another for
     database management, with options to update and add new modules to the
     database.
    """
    pathh = ""
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Attendance Tracking App")

        # ------------- BASIC APP LAYOUT -----------------

        self.geometry("1100x700")
        self.resizable(0, 0)
        self.title('Attendance Tracking System')
        self.config(background=selectionbar_color)
        icon = tk.PhotoImage(file='images/logo.png')
        self.iconphoto(True, icon)

        # ---------------- HEADER ------------------------

        self.header = tk.Frame(self, bg=header_color)
        self.header.config(highlightbackground="black", highlightthickness=4)

        self.header.place(relx=0.2, rely=0, relwidth=0.8, relheight=0.08)
        label = tk.Label(self.header, text='Your Personal HW Asisstant', font=("Arial", 16, "bold"),
                         bg=header_color, fg='white')
        label.pack(padx=10, pady=10)

        # ---------------- SIDEBAR -----------------------
        # CREATING FRAME FOR SIDEBAR
        self.sidebar = tk.Frame(self, bg=sidebar_color)
        self.sidebar.place(relx=0, rely=0, relwidth=0.2, relheight=1)

        # UNIVERSITY LOGO AND NAME
        self.brand_frame = tk.Frame(self.sidebar, bg=sidebar_color)
        self.brand_frame.place(relx=0, rely=0, relwidth=1, relheight=0.15)
        self.uni_logo = icon.subsample(9)
        logo = tk.Label(self.brand_frame, image=self.uni_logo, bg=sidebar_color)
        logo.place(x=20, y=50)

        uni_name = tk.Label(self.brand_frame,
                            text='GPT-HW',
                            bg=sidebar_color,
                            font=("", 15, "bold")
                            )
        uni_name.place(x=55, y=27, anchor="w")

        # SUBMENUS IN SIDE BAR

        # SUBMENU 1
        submenu_frame1 = tk.Frame(self.sidebar, bg=sidebar_color)
        submenu_frame1.place(relx=0, rely=0.2, relwidth=1, relheight=0.3)
        submenu1 = SidebarSubMenu(submenu_frame1,
                                  sub_menu_heading='SUBMENU 1',
                                  sub_menu_options=["Upload Question Paper",
                                                    "Edit/Comment on Question Paper",
                                                    "View Solved Question Paper"]
                                  )
        submenu1.options["Upload Question Paper"].config(
            command=lambda: self.show_frame(Frame1)
        )
        # submenu1.options["Edit/Comment on Question Paper"].config(
        #     command=lambda: self.show_frame(Frame2)
        # )
        submenu1.options["View Solved Question Paper"].config(
            command=lambda: self.show_frame(Frame3)
        )

        submenu1.place(relx=0, rely=0, relwidth=1, relheight=1)

        # # SUBMENU 2
        # submenu_frame2 = tk.Frame(self.sidebar, bg=sidebar_color)
        # submenu_frame2.place(relx=0, rely=0.55, relwidth=1, relheight=0.3)
        # submenu2 = SidebarSubMenu(submenu_frame2,
        #                           sub_menu_heading='SUBMENU 2',
        #                           sub_menu_options=["Display Frame1",
        #                                             "Display Frame2",
        #                                             "Display Frame3"]
        #                           )
        # submenu2.options["Display Frame1"].config(
        #     command=lambda: self.show_frame(Frame1)
        # )
        # submenu2.options["Display Frame2"].config(
        #     command=lambda: self.show_frame(Frame2)
        # )
        #
        # submenu2.place(relx=0, rely=0, relwidth=1, relheight=1)

        # --------------------  MULTI PAGE SETTINGS ----------------------------

        container = tk.Frame(self)
        container.config(highlightbackground="black", highlightthickness=4)
        container.place(relx=0.2, rely=0.08, relwidth=0.8, relheight=0.9)

        self.frames = {}

        for F in (Frame1,
                  Frame2,
                  Frame3
                  ):
            frame = F(container, self)
            self.frames[F] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.show_frame(Frame1)

    def show_frame(self, cont):
        """
        The function 'show_frame' is used to raise a specific frame (page) in
        the tkinter application and update the title displayed in the header.

        Parameters:
        cont (str): The name of the frame/page to be displayed.
        title (str): The title to be displayed in the header of the application.

        Returns:
        None
        """
        frame = self.frames[cont]
        frame.tkraise()


    def set_path(self, newpath, frame):
        frame2 = self.frames[frame]
        frame2.file_name = newpath


# ------------------------ MULTIPAGE FRAMES ------------------------------------
class Frame1(tk.Frame):
    file_name = ""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        print("Parent:", parent)
        print("Controller:", controller)
        self.frame1_header = tk.Frame(self, bg="Grey")
        self.frame1_header.pack(fill=tk.X)
        label = tk.Label(self.frame1_header, text='Upload Question Paper', font=("Arial", 18, "bold"),
                         bg="grey", fg='white')
        label.pack(padx=10, pady=8)
        self.upload_button = tk.Button(self, text="Upload File", command=self.open_upload_dialog)
        self.upload_button.place(relx=0.48, rely=0.12, anchor="center")
        self.edit_button = tk.Button(self, text="Edit Question Paper", command=lambda: [controller.show_frame(Frame2), controller.set_path(self.file_name, Frame2)])
        self.edit_button.place(relx=0.9, rely=0.965, anchor="center")

        self.file_uploaded_label = None  # Initialize as None

        self.image_canvas = tk.Canvas(self, width=400, height=300)
        self.image_canvas.config(bg="white", highlightbackground="black", highlightthickness=1)
        # self.image_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.image_canvas.place(relx=0.005, rely=0.15, relwidth=0.972, relheight=0.77)

        self.image_frame = tk.Frame(self.image_canvas)
        # self.image_frame.config(bg="white",highlightbackground="black", highlightthickness=1)
        self.image_canvas.create_window((0, 0), window=self.image_frame, anchor=tk.NW)

        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.image_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.image_canvas.configure(yscrollcommand=scrollbar.set)
        self.image_canvas.bind('<Configure>', self.on_canvas_configure)
        self.image_canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def open_upload_dialog(self):
        self.test = 4
        Frame1.test = self.test
        # Open file dialog for selecting PDF file
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        
        # set_path(self, newpath=file_path, frame=Frame2)
        self.file_name = os.path.basename(file_path)
        Frame1.file_name = self.file_name
        if file_path:
            # Specify the destination directory
            destination_dir = "./uploads"

            # Create the destination directory if it doesn't exist
            os.makedirs(destination_dir, exist_ok=True)

            # Generate the destination file path
            name = self.file_name.split
            destination_path = os.path.join(destination_dir, self.file_name)
            a = Frame1.file_name
            # Copy the file to the destination directory
            shutil.copy2(file_path, destination_path)

            # Store the uploaded file name in a variable
            self.uploaded_file_name = destination_path

            preprocess.pdf2img(f"./uploads/{self.file_name}")  # --> Pdf will conver and make an image folder
            self.display_images()
            preprocess.pdf2folder(
                f"./uploads/{self.file_name}")  # --> Pdf will conver and make a folder of all text files
            gpt_funs.merge_into_one_text_file(f"./uploads/text/{self.file_name.split('.')[0]}")

            # gpt_funs.format_entire_pdf("output_folder")  # --> This will meanwhile run all the files through gptapi
            # gpt_funs.merge_into_one_text_file("output_folder")  # --> This will merge final answer to show the output in a text file
        Frame1.file_name = self.file_name
        # print(Frame1.name+"hello")

    def display_images(self):
        print(os.listdir(f"./uploads/{self.file_name.split('.')[0]}/"))
        for file_path in os.listdir(f"./uploads/{self.file_name.split('.')[0]}/"):
            file_path = f"./uploads/{self.file_name.split('.')[0]}/{file_path}"
            # Open and resize the image
            image = Image.open(file_path)
            image = image.resize((820, 1000), Image.LANCZOS)

            # Create a Tkinter-compatible image object
            tk_image = ImageTk.PhotoImage(image)

            # Create a label to display the image
            image_label = tk.Label(self.image_frame, image=tk_image)
            image_label.image = tk_image
            image_label.pack()
        # condition to check if image is successfully uploaded

        # Update the size of the canvas window
        self.image_canvas.update_idletasks()
        self.image_canvas.configure(scrollregion=self.image_canvas.bbox(tk.ALL))

    def on_canvas_configure(self, event):
        self.image_canvas.configure(scrollregion=self.image_canvas.bbox(tk.ALL))

    def on_mousewheel(self, event):
        self.image_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # Example usage

    def preview_pdf(self, file_path):
        pass

print(pathh)
# obj = Frame1(Frame1, Frame1)
# obj.modify_a()
# frame1_instance = Frame1()
# frame1_instance.open_upload_dialog()  # Call the method to update file_name
# print(Frame1.file_name + "hello")
class Frame2(tk.Frame):
    file_name = ""
    def __init__(self, parent, controller, **kwargs):
        tk.Frame.__init__(self, parent)
        self.frame2_header = tk.Frame(self, bg="Grey")
        self.frame2_header.pack(fill=tk.X)
        label = tk.Label(self.frame2_header, text='Edit Questions/Add Sugggestions', font=("Arial", 18, "bold"),
                         bg="grey", fg='white')
        label.pack(padx=10, pady=8)
        self.text_area = scrolledtext.ScrolledText(self, font=("Times New Roman", 15))
        # self.text_area.insert(tk.INSERT, f'./uploads/text/{self.name}/merged.txt')
        self.text_area.place(relx=0.51, rely=0.35, relwidth=0.9, relheight=0.5, anchor="center")
        load_button = tk.Button(self, text="Load", command=self.load_text)
        load_button.place(relx=0.51, rely=0.25, relwidth=0.1, relheight=0.05, anchor="center")
        # print(Frame2.test)
        # print(Frame1.test)

    def load_text(self):
        self.text_area.insert(tk.INSERT, f'./uploads/text/{self.name}/merged.txt')
    print(file_name+"check")

class Frame3(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Frame 3', font=("Arial", 15))
        label.pack()


# ----------------------------- CUSTOM WIDGETS ---------------------------------

class SidebarSubMenu(tk.Frame):
    """
    A submenu which can have multiple options and these can be linked with
    functions.
    """

    def __init__(self, parent, sub_menu_heading, sub_menu_options):
        """
        parent: The frame where submenu is to be placed
        sub_menu_heading: Heading for the options provided
        sub_menu_operations: Options to be included in sub_menu
        """
        tk.Frame.__init__(self, parent)
        self.config(bg=sidebar_color)
        self.sub_menu_heading_label = tk.Label(self,
                                               text=sub_menu_heading,
                                               bg=sidebar_color,
                                               fg="#333333",
                                               font=("Arial", 10)
                                               )
        self.sub_menu_heading_label.place(x=30, y=10, anchor="w")

        sub_menu_sep = ttk.Separator(self, orient='horizontal')
        sub_menu_sep.place(x=30, y=30, relwidth=0.8, anchor="w")

        self.options = {}
        for n, x in enumerate(sub_menu_options):
            self.options[x] = tk.Button(self,
                                        text=x,
                                        bg=sidebar_color,
                                        font=("Arial", 9, "bold"),
                                        bd=0,
                                        cursor='hand2',
                                        activebackground='#ffffff',
                                        )
            self.options[x].place(x=30, y=45 * (n + 1), anchor="w")


app = TkinterApp()
app.mainloop()
