import cv2
import tkinter as tk
from PIL import Image, ImageTk
import threading
import random
import string


class class_drone_controller_display:
    def __init__(self, info):
        self.info = info
        self.window = tk.Tk()
        self.window.title("Flight Controller Display")
        self.window.geometry("800x480")  # Set window size to 800x480

        self.video_source = self.info.frame
        self.vid = cv2.VideoCapture(self.video_source)
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.frame_canvas = tk.Canvas(self.window, width=640, height=480)
        self.frame_canvas.grid(row=0, column=0, sticky="nsew")

        self.info_frame = tk.Frame(self.window, bg="#333333", width=160, height=480)  # Adjusted height for info frame
        self.info_frame.grid(row=0, column=1, sticky="nsew")

        self.gps_frame = tk.Frame(self.info_frame, bg="#333333", bd=2, relief=tk.SOLID)  # Box around GPS info
        self.gps_frame.pack(anchor="w", padx=8, pady=(4, 0), fill=tk.X)

        self.gps_label = tk.Label(self.gps_frame, text="GPS", anchor="w", bg="#333333", fg="white")  # GPS label
        self.gps_label.pack(anchor="w")

        self.latitude_frame = tk.Frame(self.gps_frame, bg="#333333")  # Latitude frame
        self.latitude_frame.pack(anchor="w", padx=8)

        self.latitude_label = tk.Label(self.latitude_frame, text="Latitude: Waiting for data...", anchor="w",
                                       bg="#333333", fg="white",font=("Arial", 8))  # White text color
        self.latitude_label.pack(anchor="w")

        self.longitude_frame = tk.Frame(self.gps_frame, bg="#333333")  # Longitude frame
        self.longitude_frame.pack(anchor="w", padx=8, pady=(0, 4))

        self.longitude_label = tk.Label(self.longitude_frame, text="Longitude: Waiting for data...", anchor="w",
                                        bg="#333333", fg="white", font=("Arial", 8))  # White text color
        self.longitude_label.pack(anchor="w")

        self.switch_frame = tk.Frame(self.info_frame, bg="#333333", bd=2, relief=tk.SOLID)  # Box around switch info
        self.switch_frame.pack(anchor="w", padx=8, pady=(4, 0), fill=tk.X)

        self.switch_state_label = tk.Label(self.switch_frame, text="Switch State", anchor="w", bg="#333333",
                                           fg="white")  # Switch state label
        self.switch_state_label.pack(anchor="w")

        self.switch_labels = []
        self.switch_values = [False] * 4

        self.joystick_frame_L = tk.Frame(self.info_frame, bg="#333333", bd=2,
                                         relief=tk.SOLID)  # Box around joystick L info
        self.joystick_frame_L.pack(anchor="w", padx=8, pady=(4, 0), fill=tk.X)

        self.joystick_frame_R = tk.Frame(self.info_frame, bg="#333333", bd=2,
                                         relief=tk.SOLID)  # Box around joystick R info
        self.joystick_frame_R.pack(anchor="w", padx=8, pady=(4, 0), fill=tk.X)

        self.log_text_R = tk.Text(self.info_frame, width=22, height=7, bg="#1c1c1c", fg="white", font=("Arial", 8))
        self.log_text_R.pack(anchor="w", padx=8, pady=(4, 0))

        self.update_switches()
        self.update_gps()
        self.update_joystick()  # Add call to update_joystick method
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
            switch_label.pack(anchor="w", padx=8)
            self.switch_labels.append(switch_label)

    def update_gps(self):
        # IT관 위도 경도
        latitude = 35.830622286686854
        longitude = 128.7544099722211 

        latitude_text = f"Latitude: {latitude:.5f}"
        longitude_text = f"Longitude: {longitude:.5f}"

        self.latitude_label.config(text=latitude_text)
        self.longitude_label.config(text=longitude_text)

        self.window.after(1000, self.update_gps)  # Update every 1 second

    def update_joystick(self):
        # Simulate joystick data
        joystick_values_L = {
            'x': random.randint(0, 100),
            'y': random.randint(0, 100),
            'switch': random.choice([True, False])
        }
        joystick_values_R = {
            'x': random.randint(0, 100),
            'y': random.randint(0, 100),
            'switch': random.choice([True, False])
        }

        # Update labels for joystick L
        self.update_joystick_labels(self.joystick_frame_L, "Joystick L", joystick_values_L)

        # Update labels for joystick R
        self.update_joystick_labels(self.joystick_frame_R, "Joystick R", joystick_values_R)

        # Update log for joystick R
        log_message = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        self.log_text_R.insert(tk.END, log_message + "\n")
        self.log_text_R.see(tk.END)  # Scroll to the bottom

        self.window.after(1000, self.update_joystick)  # Update every 1 second

    def update_joystick_labels(self, frame, name, values):
        for label in frame.winfo_children():
            label.destroy()

        joystick_label = tk.Label(frame, text=name, anchor="w", bg="#333333", fg="white")
        joystick_label.pack(anchor="w")

        x_label = tk.Label(frame, text=f"x: {values['x']}", anchor="w", bg="#333333", fg="white")
        x_label.pack(anchor="w", padx=(8, 0))

        y_label = tk.Label(frame, text=f"y: {values['y']}", anchor="w", bg="#333333", fg="white")
        y_label.pack(anchor="w", padx=(8, 0))

        switch_label = tk.Label(frame, text=f"switch: {'ON' if values['switch'] else 'OFF'}", anchor="w",
                                bg="#333333", fg="white")
        switch_label.pack(anchor="w", padx=(8, 0))



