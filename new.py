import tkinter as tk
from tkinter import filedialog
import cv2
import torch
from terminal import Terminal
from clock import Clock
from codeline import code_lines
import subprocess
from PIL import Image, ImageTk

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

class HumanDetectionApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Human Detection")

        self.master.attributes('-fullscreen', True)
        self.master.bind("<Escape>", self.exit_fullscreen)
        

        self.master.configure(bg="black")

        self.clock = Clock(master)

        self.terminal = Terminal(master)
        self.terminal.place(relx=0.65, rely=0.53, anchor=tk.CENTER, width=1000, height=690)

        self.master.after(100, lambda: self.terminal.type_code(code_lines))

        self.label = tk.Label(master, text="HUMAN + OBJECT DETECTOR", fg="cyan", bg="black", font=("Recharge Rg", 23, "bold"))
        self.label.place(relx=0.5, rely=0.07, anchor=tk.CENTER)

        self.label = tk.Label(master, text="Choose an option:", fg="cyan", bg="black", font=("Recharge Rg", 16, "bold"))
        self.label.place(relx=0.2, rely=0.15, anchor=tk.CENTER)

        button_width = 20
        button_height = 2

        self.btn_camera = tk.Button(master, text="Launch Camera", command=self.launch_camera, font=("Helvetica", 16, "bold"),
                                     bg="cyan", fg="black", width=button_width, height=button_height)
        self.btn_camera.place(relx=0.2, rely=0.23, anchor=tk.CENTER)

        self.btn_droidcam = tk.Button(master, text="Connect to MyPhone", command=self.start_hog_detection, font=("Helvetica", 16, "bold"),
                                       bg="cyan", fg="black", width=button_width, height=button_height)
        self.btn_droidcam.place(relx=0.2, rely=0.33, anchor=tk.CENTER)

        self.btn_video = tk.Button(master, text="Select Video", command=self.select_video, font=("Helvetica", 16, "bold"),
                                   bg="cyan", fg="black", width=button_width, height=button_height)
        self.btn_video.place(relx=0.2, rely=0.43, anchor=tk.CENTER)

        self.btn_image = tk.Button(master, text="Select Image", command=self.select_image, font=("Helvetica", 16, "bold"),
                                   bg="cyan", fg="black", width=button_width, height=button_height)
        self.btn_image.place(relx=0.2, rely=0.53, anchor=tk.CENTER)

        self.btn_ppt = tk.Button(master, text="Show PowerPoint", command=self.show_ppt, font=("Helvetica", 16, "bold"),
                                 bg="cyan", fg="black", width=button_width, height=button_height)
        self.btn_ppt.place(relx=0.2, rely=0.63, anchor=tk.CENTER)

        self.image_path = "loading5.png"
        self.original_image = Image.open(self.image_path).resize((220, 220), Image.LANCZOS)
        self.angle = 0

        self.tk_image = ImageTk.PhotoImage(self.original_image)

        self.image_label = tk.Label(master, image=self.tk_image, bg="black")
        self.image_label.place(relx=0.2, rely=0.85, anchor=tk.CENTER)

        self.rotate_image()

        self.video_source = None
        self.hog_detector = cv2.HOGDescriptor()
        self.hog_detector.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    def rotate_image(self):
        self.angle = (self.angle + 5) % 360
        rotated_image = self.original_image.rotate(self.angle, expand=True)
        self.tk_image = ImageTk.PhotoImage(rotated_image)

        self.image_label.configure(image=self.tk_image)
        self.image_label.image = self.tk_image

        self.master.after(50, self.rotate_image)

    def launch_camera(self):
        self.video_source = 0
        self.start_detection()

    def start_hog_detection(self):
        self.video_source = 1 
        cap = cv2.VideoCapture(self.video_source)
        cv2.namedWindow("HOG Human Detection", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("HOG Human Detection", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            boxes, _ = self.hog_detector.detectMultiScale(frame, winStride=(8, 8))

            count = 0
            for (x, y, w, h) in boxes:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                count += 1

            cv2.putText(frame, f'Count: {count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.imshow('HOG Human Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def select_video(self):
        self.video_source = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi")])
        if self.video_source:
            self.start_detection()

    def select_image(self):
        image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if image_path:
            self.detect_image(image_path)

    def show_ppt(self):
        ppt_path = "ppt.pptx"

        try:
            subprocess.Popen([r'C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE', ppt_path])
        except Exception as e:
            print(f"Error opening PowerPoint: {e}")

    def start_detection(self):
        cap = cv2.VideoCapture(self.video_source)
        cv2.namedWindow("Human Detection", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Human Detection", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            results = model(frame)
            results.render()
            count = (results.pandas().xyxy[0]['name'] == 'person').sum()
            cv2.putText(frame, f'Count: {count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Human Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def exit_fullscreen(self, event=None):
        self.master.attributes('-fullscreen', False)

if __name__ == "__main__":
    root = tk.Tk()
    app = HumanDetectionApp(root)
    root.mainloop()
