import tkinter as tk
from tkinter import messagebox
from route import Route
from RailwayVehicles import Train, Tram


class VehicleGUI:
    def __init__(self, root, pojazd, current_route):
        self.root = root
        self.pojazd = pojazd
        self.current_route = current_route
        root.title("Driver Simulator (GUI)")
        self.lbl_type = tk.Label(
            root, text=f"Vehicle Type: {self.pojazd.__class__.__name__}")
        self.lbl_type.grid(row=0, column=0, columnspan=2, pady=5)

        self.lbl_id = tk.Label(root, text=f"Vehicle: {self.pojazd.id}")
        self.lbl_id.grid(row=1, column=0, columnspan=2, pady=5)

        self.lbl_speed = tk.Label(root, text="Speed: 0 km/h")
        self.lbl_speed.grid(row=2, column=0, sticky="w", padx=10)

        self.lbl_doors = tk.Label(root, text="Doors: OPEN")
        self.lbl_doors.grid(row=2, column=1, sticky="w", padx=10)

        self.lbl_vagons = tk.Label(root, text="Wagons: none")
        self.lbl_vagons.grid(row=3, column=0, sticky="w", padx=10)
        self.lbl_capacity = tk.Label(
            root, text=f"Capacity: {self.pojazd.capacity}")
        self.lbl_capacity.grid(row=3, column=1, sticky="w", padx=10)

        self.lbl_temp = tk.Label(root, text="Engine temperature: 0.0 °C")
        self.lbl_temp.grid(row=4, column=0, columnspan=2, sticky="w", padx=10)
        self.lbl_brake = tk.Label(root, text="Brake value: 0.0")
        self.lbl_brake.grid(row=5, column=0, columnspan=2, sticky="w", padx=10)
        self.lbl_distance = tk.Label(root, text="Distance: ")
        self.lbl_distance.grid(
            row=7, column=0, columnspan=2, sticky="w", padx=10)
        self.diagnostic_status = "Diagnostics: not run yet"
        self.lbl_status = tk.Label(root, text=self.diagnostic_status)
        self.lbl_status.grid(
            row=8, column=0, columnspan=2, sticky="w", padx=10)

        btn_frame = tk.Frame(root)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=10)

        tk.Button(btn_frame, text="Accelerate (+20)",
                  command=self.accelerate).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Brake",
                  command=self.brake).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Close doors",
                  command=self.close_doors).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Open doors",
                  command=self.open_doors).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Diagnostics", command=self.system_check).grid(
            row=1, column=0, columnspan=2, pady=5)

        tk.Button(btn_frame, text="Exit", command=root.quit).grid(
            row=1, column=2, columnspan=2, pady=5)

        if hasattr(self.pojazd, "vagon_number"):
            tk.Button(btn_frame, text="Connect wagon",
                      command=self.connect_vagon).grid(row=2, column=0, padx=5, pady=5)
            tk.Button(btn_frame, text="Disconnect wagon",
                      command=self.disconnect_vagon).grid(row=2, column=1, padx=5, pady=5)
        if hasattr(self.pojazd, "ring_bell"):
            tk.Button(btn_frame, text="Ring bell",
                      command=self.ring_bell_gui).grid(row=2, column=2, padx=5, pady=5)

        self.update_ui()

    def accelerate(self):
        if not self.pojazd.accelerate():
            messagebox.showwarning(
                "Warning", "Starting with doors open is not allowed! Close the doors first.")
        self.refresh_labels()

    def brake(self):
        self.pojazd.brake()
        self.refresh_labels()

    def close_doors(self):
        self.pojazd.door_open = False
        messagebox.showinfo("Doors", "Doors have been closed.")
        self.refresh_labels()

    def open_doors(self):
        self.pojazd.open_door()
        self.refresh_labels()

    def connect_vagon(self):
        if hasattr(self.pojazd, "connect_vagon"):
            try:
                self.pojazd.connect_vagon(1)
            except Exception:
                messagebox.showerror("Error", "Failed to connect wagon")
        else:
            messagebox.showinfo("Info", "This vehicle cannot connect wagons")
        self.refresh_labels()

    def disconnect_vagon(self):
        if hasattr(self.pojazd, "disconnect_vagon"):
            try:
                self.pojazd.disconnect_vagon(1)
            except Exception:
                messagebox.showerror("Error", "Failed to disconnect wagon")
        else:
            messagebox.showinfo(
                "Info", "This vehicle has no wagons to disconnect")
        self.refresh_labels()

    def ring_bell_gui(self):
        if hasattr(self.pojazd, "ring_bell"):
            try:
                self.pojazd.ring_bell()
                messagebox.showinfo("Bell", "Bell rung")
            except Exception:
                messagebox.showerror("Error", "Failed to ring bell")
        else:
            messagebox.showinfo("Info", "This vehicle has no bell")
        self.refresh_labels()

    def system_check(self):
        failed_sensors = self.pojazd.system_check()
        if failed_sensors:
            self.diagnostic_status = (
                "Diagnostics: FAILED - " + ", ".join(failed_sensors)
            )
        else:
            self.diagnostic_status = "Diagnostics: OK"

        self.refresh_labels()

    def refresh_labels(self):
        self.lbl_speed.config(
            text=f"Speed: {self.pojazd.now_v} km/h / {self.pojazd.max_v} km/h")
        stan = "OPEN" if self.pojazd.door_open else "CLOSED"
        self.lbl_doors.config(text=f"Doors: {stan}")
        wagony = getattr(self.pojazd, "vagon_number", None)
        self.lbl_vagons.config(
            text=f"Wagons: {wagony}" if wagony is not None else "Wagons: none")
        self.lbl_capacity.config(text=f"Capacity: {self.pojazd.capacity}")
        self.lbl_temp.config(
            text=f"Engine temperature: {self.pojazd.sensors[0].actual_value} °C")
        self.lbl_brake.config(
            text=f"Brake value: {self.pojazd.sensors[1].actual_value}")
        self.lbl_distance.config(
            text=f"Distance: {self.pojazd.total_dystans:.2f} km")
        self.lbl_status.config(text=self.diagnostic_status)
    def update_ui(self):

        time_step = 10
        self.current_route.progress(vehicle=self.pojazd, delta_time=time_step)
        self.system_check()

        if self.current_route.station == True:
            self.refresh_labels()

            messagebox.showinfo(
                "Destination", "You have reached the destination")
        self.refresh_labels()

        self.root.after(2000, self.update_ui)


def uruchom_gui():
    chooser = tk.Tk()
    chooser.title("Choose vehicle")
    chooser.resizable(False, False)

    selected_type = tk.StringVar(value="train")

    tk.Label(chooser, text="Select vehicle type to start:").pack(
        padx=16, pady=(16, 8))
    tk.Radiobutton(chooser, text="Train", variable=selected_type,
                   value="train").pack(anchor="w", padx=16)
    tk.Radiobutton(chooser, text="Tram", variable=selected_type,
                   value="tram").pack(anchor="w", padx=16)

    result = {"value": None}

    def confirm_choice():
        result["value"] = selected_type.get()
        chooser.destroy()

    tk.Button(chooser, text="Start", command=confirm_choice).pack(pady=16)
    chooser.mainloop()

    if result["value"] == "tram":
        pojazd = Tram(id="Pesa tram", max_v=70,
                      now_v=0, door_open=True, capacity=150)
    else:
        pojazd = Train(id="Pesa train", max_v=160, now_v=0,
                       door_open=True, capacity=300, vagon_number=4, max_vagon_number=6)
    current_route = Route(distance=5, position=0, time=30)

    root = tk.Tk()
    app = VehicleGUI(root, pojazd, current_route)
    root.mainloop()
