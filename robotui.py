#robotui.py
import tkinter as tk


class MotorControlUi:
    def __init__(self, master, num_motors):
        self.master = master
        master.title("   DOF6   ")

        self.num_motors = num_motors
        self.frame = tk.Frame(master)
        self.frame.pack()

        self.labels = []
        self.target_entries = []

        self.pos_flags = [0] * self.num_motors
        self.neg_flags = [0] * self.num_motors
        self.go_to_flags = [0] * self.num_motors
        self.go_to_park_flags = [0] * self.num_motors
        self.go_to_home_flags = [0] * self.num_motors
        self.go_to_x_flags = [0] * self.num_motors
        self.go_to_y_flags = [0] * self.num_motors
        self.go_to_z_flags = [0] * self.num_motors
        self.go_to_stop_flags = [0] * self.num_motors

        self.go_to_buttons = []
        self.go_to_job_ids = []

        for i in range(self.num_motors):
            positive_button = tk.Button(self.frame, text=f"M{i + 1} Pos", fg="white", bg="black")
            positive_button.grid(row=i, column=0, padx=10)
            positive_button.bind("<ButtonPress>", lambda event, index=i: self.pos_flag(event, index, 1))
            positive_button.bind("<ButtonRelease>", lambda event, index=i: self.pos_flag(event, index, 0))

            negative_button = tk.Button(self.frame, text=f"M{i + 1} Neg", fg="white", bg="black")
            negative_button.grid(row=i, column=1, padx=10)
            negative_button.bind("<ButtonPress>", lambda event, index=i: self.neg_flag(event, index, 1))
            negative_button.bind("<ButtonRelease>", lambda event, index=i: self.neg_flag(event, index, 0))

            # Labels on the right
            label = tk.Label(self.frame, text=f" 0 ", font=("Helvetica", 16), fg="white", bg="red", width=5)
            label.grid(row=i, column=2, padx=10)
            self.labels.append(label)

            entry = tk.Entry(self.frame, width=5)
            entry.grid(row=i, column=3, padx=10)
            self.target_entries.append(entry)

            go_to_button = tk.Button(self.frame, text=f"Go Pos {i + 1}", fg="white", bg="purple")
            go_to_button.grid(row=i, column=4, padx=10)
            go_to_button.bind("<ButtonPress>", lambda event, index=i: self.go_to_flag(event, index, 1))
            go_to_button.bind("<ButtonRelease>", lambda event, index=i: self.go_to_flag(event, index, 0))

            go_to_home = tk.Button(self.frame, text=f"Home", fg="white", bg="blue", width=7)
            go_to_home.grid(row=0, column=5, padx=10)
            go_to_home.bind("<ButtonPress>", lambda event, index=i: self.go_to_home_flag(event, index, 1))
            go_to_home.bind("<ButtonRelease>", lambda event, index=i: self.go_to_home_flag(event, index, 0))

            go_to_park = tk.Button(self.frame, text=f" Park ", fg="white", bg="blue", width=7)
            go_to_park.grid(row=1, column=5, padx=10)
            go_to_park.bind("<ButtonPress>", lambda event, index=i: self.go_to_park_flag(event, index, 1))
            go_to_park.bind("<ButtonRelease>", lambda event, index=i: self.go_to_park_flag(event, index, 0))

            go_to_x = tk.Button(self.frame, text=f"X", fg="white", bg="orange", width=7)
            go_to_x.grid(row=2, column=5, padx=10)
            go_to_x.bind("<ButtonPress>", lambda event, index=i: self.go_to_x_flag(event, index, 1))
            go_to_x.bind("<ButtonRelease>", lambda event, index=i: self.go_to_x_flag(event, index, 0))

            go_to_y = tk.Button(self.frame, text=f"Y", fg="white", bg="orange", width=7)
            go_to_y.grid(row=3, column=5, padx=10)
            go_to_y.bind("<ButtonPress>", lambda event, index=i: self.go_to_y_flag(event, index, 1))
            go_to_y.bind("<ButtonRelease>", lambda event, index=i: self.go_to_y_flag(event, index, 0))

            go_to_z = tk.Button(self.frame, text=f"Z", fg="white", bg="orange", width=7)
            go_to_z.grid(row=4, column=5, padx=10)
            go_to_z.bind("<ButtonPress>", lambda event, index=i: self.go_to_z_flag(event, index, 1))
            go_to_z.bind("<ButtonRelease>", lambda event, index=i: self.go_to_z_flag(event, index, 0))

            do_stop_button = tk.Button(self.frame, text=f"STOP", fg="white", bg="red", width=7)
            do_stop_button.grid(row=5, column=5, padx=10)
            do_stop_button.bind("<ButtonPress>", lambda event, index=i: self.go_to_stop_flag(event, index, 1))
            do_stop_button.bind("<ButtonRelease>", lambda event, index=i: self.go_to_stop_flag(event, index, 0))

    def pos_flag(self, event, index, value):
        # Bu fonksiyon basıldığında veya bırakıldığında çağrılır.
        # index, hangi düğmenin etkilendiğini belirtir.
        # value, basıldığında 1 veya bırakıldığında 0 olmalıdır.
        self.pos_flags[index] = value
        # print(f"M{index + 1} Pos Flag: {value}")

    def neg_flag(self, event, index, value):
        self.neg_flags[index] = value
        # print(f"M{index + 1} Neg Flag: {value}")

    def go_to_flag(self, event, index, value):
        self.go_to_flags[index] = value

    def go_to_park_flag(self, event, index, value):
        self.go_to_park_flags[index] = value

    def go_to_home_flag(self, event, index, value):
        self.go_to_home_flags[index] = value

    def go_to_x_flag(self, event, index, value):
        self.go_to_x_flags[index] = value

    def go_to_y_flag(self, event, index, value):
        self.go_to_y_flags[index] = value

    def go_to_z_flag(self, event, index, value):
        self.go_to_z_flags[index] = value

    def go_to_stop_flag(self, event, index, value):
        self.go_to_stop_flags[index] = value

    def get_target_entries(self):
        return self.target_entries

    def run(self):
        self.master.mainloop()

