import cv2
import tkinter as tk
from PIL import Image, ImageTk
import threading
import random


class FlightDisplayApp:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.window.geometry("800x480")  # Set window size to 800x480

        self.video_source = video_source
        self.vid = cv2.VideoCapture(self.video_source)
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.frame_canvas = tk.Canvas(window, width=640, height=480)
        self.frame_canvas.grid(row=0, column=0, sticky="nsew")

        self.info_frame = tk.Frame(window, bg="#333333", width=160, height=480)  # Adjusted width for info frame
        self.info_frame.grid(row=0, column=1, sticky="nsew")

        self.gps_frame = tk.Frame(self.info_frame, bg="#333333", bd=2, relief=tk.SOLID)  # Box around GPS info
        self.gps_frame.pack(anchor="w", padx=8, pady=(8, 0))

        self.gps_label = tk.Label(self.gps_frame, text="GPS", anchor="w", bg="#333333", fg="white")  # GPS label
        self.gps_label.pack(anchor="w")

        self.latitude_frame = tk.Frame(self.gps_frame, bg="#333333")  # Latitude frame
        self.latitude_frame.pack(anchor="w", padx=8)

        self.latitude_label = tk.Label(self.latitude_frame, text="Latitude: Waiting for data...", anchor="w",
                                       bg="#333333", fg="white")  # White text color
        self.latitude_label.pack(anchor="w")

        self.longitude_frame = tk.Frame(self.gps_frame, bg="#333333")  # Longitude frame
        self.longitude_frame.pack(anchor="w", padx=8, pady=(0, 8))

        self.longitude_label = tk.Label(self.longitude_frame, text="Longitude: Waiting for data...", anchor="w",
                                        bg="#333333", fg="white")  # White text color
        self.longitude_label.pack(anchor="w")

        self.switch_frame = tk.Frame(self.info_frame, bg="#333333", bd=2, relief=tk.SOLID)  # Box around switch info
        self.switch_frame.pack(anchor="w", padx=8, pady=(8, 0))

        self.switch_state_label = tk.Label(self.switch_frame, text="Switch State", anchor="w", bg="#333333",
                                           fg="white")  # Switch state label
        self.switch_state_label.pack(anchor="w", padx=8, pady=(0, 8))

        self.switch_labels = []
        self.switch_values = [False] * 4

        self.update_switches()
        self.update_gps()

        self.update()

        self.window.mainloop()

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (640, 480))  # Resize frame to 640x480
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.frame_canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(10, self.update)

    def update_switches(self):
        for label in self.switch_labels:
            label.destroy()

        self.switch_labels = []
        for i, switch_value in enumerate(self.switch_values):
            switch_label = tk.Label(self.switch_frame, text=f"Switch {i + 1}: {'ON' if switch_value else 'OFF'}",
                                    anchor="w", bg="#333333", fg="white")  # White text color
            switch_label.pack(anchor="w", padx=8, pady=(0, 8))
            self.switch_labels.append(switch_label)

    def update_gps(self):
        # Dummy GPS data for demonstration
        latitude = random.uniform(-90, 90)
        longitude = random.uniform(-180, 180)

        latitude_text = "Latitude: {:.2f}".format(latitude)
        longitude_text = "Longitude: {:.2f}".format(longitude)

        self.latitude_label.config(text=latitude_text)
        self.longitude_label.config(text=longitude_text)

        self.window.after(5000, self.update_gps)  # Update every 5 seconds


if __name__ == "__main__":
    # Create a window and pass it to the application object
    root = tk.Tk()
    app = FlightDisplayApp(root, "Flight Display", "C:\\Users\\ANTL\\Documents\\카카오톡 받은 파일\\KakaoTalk_20240415_163531080.jpg")  # Set your video source
