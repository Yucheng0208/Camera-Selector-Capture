import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import datetime

class SimpleCaptureApp:
    def __init__(self, window, window_title="單鍵快速拍照工具", language='zh'):
        self.window = window
        self.language = language # 'zh' for Chinese, 'en' for English
        self.set_language_strings() # Set initial language strings

        self.window.title(self.lang['app_title'])
        self.window.geometry("700x650") # Adjust window size for new input

        self.vid = None # Initialize camera object as None
        self.camera_index = 0 # Default camera index

        self.output_folder = os.path.join(os.getcwd(), self.lang['default_folder_name']) # Default output folder
        self.photo_count = 0 # Photo counter

        self.setup_ui()
        self.open_camera(self.camera_index) # Open camera with default index
        self.update_frame() # Start updating the camera feed

        # Set up cleanup when the window is closed
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        # Bind the spacebar key to the capture function
        self.window.bind("<space>", self.capture_image_event)
        self.window.bind("<Escape>", self.on_escape_key) # Bind ESC key to close

        # Ensure the default folder exists
        os.makedirs(self.output_folder, exist_ok=True)
        print(f"{self.lang['default_folder_info']}: {self.output_folder}")

    def set_language_strings(self):
        # All translatable strings are defined here
        if self.language == 'zh':
            self.lang = {
                'app_title': "單鍵快速拍照工具",
                'folder_label': "照片儲存資料夾:",
                'select_folder_btn': "選擇資料夾",
                'camera_index_label': "攝影機編號 (0, 1, ...):",
                'apply_camera_btn': "應用攝影機",
                'instruction_label': "按下 **空白鍵** 拍照\n按下 **ESC 鍵** 退出",
                'status_waiting': "等待按下空白鍵...",
                'status_saved': "已拍照並儲存到:",
                'status_error_capture': "錯誤: 無法擷取影像。",
                'status_folder_set': "照片將儲存到:",
                'error_title': "錯誤",
                'camera_error': "無法開啟攝影機 (編號 {index})。請確認攝影機已連接且未被其他程式佔用。",
                'missing_libs_title': "錯誤",
                'missing_libs_msg': "缺少必要的函式庫！\n請執行以下指令安裝：\n`pip install opencv-python Pillow`",
                'select_folder_dialog_title': "選擇照片儲存資料夾",
                'default_folder_name': "captured_photos",
                'default_folder_info': "預設照片儲存資料夾"
            }
        else: # Default to English
            self.lang = {
                'app_title': "Single-Key Quick Photo Tool",
                'folder_label': "Photo Save Folder:",
                'select_folder_btn': "Select Folder",
                'camera_index_label': "Camera Index (0, 1, ...):",
                'apply_camera_btn': "Apply Camera",
                'instruction_label': "Press **Spacebar** to capture\nPress **ESC** to exit",
                'status_waiting': "Waiting for Spacebar...",
                'status_saved': "Photo captured and saved to:",
                'status_error_capture': "Error: Could not capture image.",
                'status_folder_set': "Photos will be saved to:",
                'error_title': "Error",
                'camera_error': "Could not open camera (index {index}). Please ensure it's connected and not in use by another application.",
                'missing_libs_title': "Error",
                'missing_libs_msg': "Missing required libraries!\nPlease install them using:\n`pip install opencv-python Pillow`",
                'select_folder_dialog_title': "Select Photo Save Folder",
                'default_folder_name': "captured_photos",
                'default_folder_info': "Default photo save folder"
            }
        # Update UI elements with new language if they exist
        if hasattr(self, 'folder_path_label'):
            self.window.title(self.lang['app_title'])
            # Re-configure existing UI elements with new language
            tk.Label(self.control_frame, text=self.lang['folder_label']).grid(row=0, column=0, sticky='w')
            self.select_folder_btn.config(text=self.lang['select_folder_btn'])
            tk.Label(self.control_frame, text=self.lang['camera_index_label']).grid(row=1, column=0, sticky='w')
            self.apply_camera_btn.config(text=self.lang['apply_camera_btn'])
            self.instruction_label.config(text=self.lang['instruction_label'])
            self.status_label.config(text=self.lang['status_waiting'])

    def setup_ui(self):
        # --- Top control area ---
        self.control_frame = tk.Frame(self.window, padx=10, pady=10)
        self.control_frame.pack(side=tk.TOP, fill=tk.X)

        # Folder selection row
        tk.Label(self.control_frame, text=self.lang['folder_label']).grid(row=0, column=0, sticky='w', pady=2)
        self.folder_path_label = tk.Label(self.control_frame, text=self.output_folder, width=40, anchor="w")
        self.folder_path_label.grid(row=0, column=1, padx=5, pady=2)

        self.select_folder_btn = tk.Button(self.control_frame, text=self.lang['select_folder_btn'], command=self.select_output_folder)
        self.select_folder_btn.grid(row=0, column=2, padx=5, pady=2)

        # Camera index selection row
        tk.Label(self.control_frame, text=self.lang['camera_index_label']).grid(row=1, column=0, sticky='w', pady=2)
        self.camera_index_entry = tk.Entry(self.control_frame, width=5)
        self.camera_index_entry.insert(0, str(self.camera_index)) # Set default value
        self.camera_index_entry.grid(row=1, column=1, sticky='w', padx=5, pady=2)

        self.apply_camera_btn = tk.Button(self.control_frame, text=self.lang['apply_camera_btn'], command=self.apply_camera_index)
        self.apply_camera_btn.grid(row=1, column=2, sticky='w', padx=5, pady=2)


        # --- Camera preview area ---
        self.canvas = tk.Label(self.window, borderwidth=2, relief="groove")
        self.canvas.pack(pady=10)

        # --- Instructions and status area ---
        self.instruction_label = tk.Label(self.window, text=self.lang['instruction_label'], font=("Helvetica", 14, "bold"))
        self.instruction_label.pack(pady=10)

        self.status_label = tk.Label(self.window, text=self.lang['status_waiting'], fg="blue")
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

    def open_camera(self, index):
        """Opens the camera at the given index."""
        if self.vid and self.vid.isOpened():
            self.vid.release() # Release existing camera if any

        try:
            self.vid = cv2.VideoCapture(index)
            if not self.vid.isOpened():
                raise ValueError("Camera not found or in use.")
            self.camera_index = index
            self.status_label.config(text=f"攝影機 {self.camera_index} 已開啟。", fg="blue")
        except Exception:
            messagebox.showerror(self.lang['error_title'], self.lang['camera_error'].format(index=index))
            self.vid = None # Ensure vid is None if opening fails
            self.status_label.config(text=f"無法開啟攝影機 {index}。", fg="red")


    def apply_camera_index(self):
        """Applies the camera index entered by the user."""
        try:
            new_index = int(self.camera_index_entry.get())
            if new_index != self.camera_index:
                self.open_camera(new_index)
        except ValueError:
            messagebox.showerror(self.lang['error_title'], "請輸入有效的數字作為攝影機編號。")
        except Exception as e:
            messagebox.showerror(self.lang['error_title'], f"切換攝影機時發生錯誤: {e}")


    def select_output_folder(self):
        """Allows user to select the output directory for photos."""
        new_folder = filedialog.askdirectory(initialdir=self.output_folder, title=self.lang['select_folder_dialog_title'])
        if new_folder:
            self.output_folder = new_folder
            self.folder_path_label.config(text=self.output_folder)
            os.makedirs(self.output_folder, exist_ok=True) # Ensure selected folder exists
            self.photo_count = 0 # Reset photo count for the new folder
            self.status_label.config(text=f"{self.lang['status_folder_set']} {self.output_folder}", fg="green")
            print(f"{self.lang['status_folder_set']} {self.output_folder}")

    def update_frame(self):
        """Reads a frame from the camera and updates the UI display."""
        if self.vid and self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                self.current_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Convert BGR to RGB

                # Resize image to fit display while maintaining aspect ratio
                img_height, img_width, _ = self.current_frame.shape
                aspect_ratio = img_width / img_height
                new_width = 640
                new_height = int(new_width / aspect_ratio)
                if new_height > 480:
                    new_height = 480
                    new_width = int(new_height * aspect_ratio)

                self.current_frame = cv2.resize(self.current_frame, (new_width, new_height))

                img = Image.fromarray(self.current_frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.canvas.imgtk = imgtk # Keep a reference!
                self.canvas.config(image=imgtk)
            else:
                self.canvas.config(image='') # Clear canvas if no frame
                self.status_label.config(text=f"無法從攝影機 {self.camera_index} 讀取幀，請檢查。", fg="red")
        else:
            self.canvas.config(image='') # Clear canvas if no camera
            # self.status_label.config(text="攝影機未開啟或無法連接。", fg="red") # Don't spam this if already showing an error

        self.window.after(10, self.update_frame) # Update every 10 milliseconds

    def capture_image_event(self, event=None):
        """Captures an image when the spacebar is pressed."""
        if hasattr(self, 'current_frame') and self.current_frame is not None and self.vid and self.vid.isOpened():
            self.photo_count += 1
            count = self.photo_count

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"photo_{timestamp}_{count:04d}.jpg"
            filepath = os.path.join(self.output_folder, filename)

            # Convert RGB back to BGR for saving with cv2.imwrite
            bgr_frame = cv2.cvtColor(self.current_frame, cv2.COLOR_RGB2BGR)
            cv2.imwrite(filepath, bgr_frame)
            self.status_label.config(text=f"{self.lang['status_saved']} {filepath}", fg="green")
            print(f"{self.lang['status_saved']} {filepath}")
        else:
            self.status_label.config(text=self.lang['status_error_capture'], fg="red")

    def on_escape_key(self, event=None):
        """Handles closing the app when ESC is pressed."""
        self.on_closing()

    def on_closing(self):
        """Releases camera resources when the window is closed."""
        if self.vid and self.vid.isOpened():
            self.vid.release()
        self.window.destroy()

# --- Main program execution ---
if __name__ == "__main__":
    # Check for necessary libraries
    try:
        import cv2
        from PIL import Image, ImageTk
    except ImportError:
        root = tk.Tk()
        root.withdraw() # Hide main window
        messagebox.showerror("錯誤", "缺少必要的函式庫！\n請執行以下指令安裝：\n`pip install opencv-python Pillow`")
        root.destroy()
        exit()

    # Pop up language selection dialog
    language_choice = messagebox.askyesno(
        "Language Selection / 語言選擇",
        "Would you like to use English?\n\n是否使用中文？\n(No for Chinese / 是為中文)",
        icon='question'
    )

    if language_choice: # If Yes (True), use English
        selected_language = 'en'
    else: # If No (False), use Chinese
        selected_language = 'zh'

    root = tk.Tk()
    app = SimpleCaptureApp(root, language=selected_language)
    root.mainloop()
