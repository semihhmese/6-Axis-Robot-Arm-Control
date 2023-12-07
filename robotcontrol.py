#robotcontrol.py
from robotui import MotorControlUi
import tkinter as tk

step_value = 1
acceleration = 0.1  # İvme değeri (gerektiğinde ayarlayın)
deceleration = 0.1  # Yavaşlama değeri (gerektiğinde ayarlayın)

class RobotControl:
    def __init__(self, num_motors):
        self.root = tk.Tk()
        self.motor_control = MotorControlUi(self.root, num_motors)
        self.motor_values = [0] * num_motors
        self.target_entries = self.motor_control.get_target_entries()
        self.go_to_job_ids = [None] * num_motors
        self.update_motor_values()
        self.motor_control.run()
        self.motor_speeds = [0] * num_motors

    def update_motor_values(self):
        for i in range(len(self.motor_values)):
            if self.motor_control.pos_flags[i] == 1:
                self.do_pos_button(i)
            elif self.motor_control.neg_flags[i] == 1:
                self.do_neg_button(i)
            elif self.motor_control.go_to_flags[i] == 1:
                self.start_go_to_position(i)
            elif self.motor_control.go_to_home_flags[i] == 1:
                self.go_to_home()
            elif self.motor_control.go_to_park_flags[i] == 1:
                self.go_to_park()

            # Update the label in MotorControlUi with the current motor value
            self.motor_control.labels[i].config(text=f" {self.motor_values[i]} ")
            self.motor_speeds[i] = self.calculate_motor_speed(i)

        # Schedule the update every 100 milliseconds (adjust as needed)
        self.root.after(100, self.update_motor_values)

    def calculate_motor_speed(self, idx):
        # Hız hesaplama mantığını buraya ekleyin
        # Örneğin, belirli bir zaman aralığında geçen konum değişikliğini kullanabilirsiniz.
        # Şu anlık hız = (Şu anki konum - Önceki konum) / Zaman aralığı

        # Örneğin:
        time_interval = 0.1  # Örneğin her 100 milisaniyede bir güncelle
        current_position = self.motor_values[idx]
        previous_position = self.motor_values[idx] - 1  # Önceki konumu belirleme için örnek değer
        speed = (current_position - previous_position) / time_interval

        return speed

    def do_pos_button(self, idx):
        self.motor_values[idx] += step_value

    def do_neg_button(self, idx):
        self.motor_values[idx] -= step_value

    def start_go_to_position(self, idx):
        try:
            target_position = int(self.target_entries[idx].get())
            self.go_to_job_ids[idx] = self.root.after(100,
                    lambda idx=idx, target=target_position: self.go_to_position(idx, target_position))
        except ValueError:
            print(f"Invalid input for Motor {idx + 1} target position.")

    def go_to_position(self, idx, target_position):
        current_position = self.motor_values[idx]
        step = step_value if current_position < target_position else -step_value



        # if self.motor_control.go_to_stop_flags[idx] == 1:
        # TODO: Motoru durdur
        #     pass

        if current_position != target_position:
            distance_to_target = abs(target_position - current_position)
            acceleration_steps = int((100 * acceleration) ** 0.5)
            deceleration_steps = int((100 * deceleration) ** 0.5)

            total_steps = acceleration_steps + deceleration_steps
            constant_speed_steps = max(0, distance_to_target - total_steps)

            if acceleration_steps > 0:
                # İvme aşaması
                self.motor_values[idx] += step
                self.update_label(idx)
                acceleration_steps -= 1
            elif constant_speed_steps > 0:
                # Sabit hız aşaması
                self.motor_values[idx] += step
                self.update_label(idx)
                constant_speed_steps -= 1
            elif deceleration_steps > 0:
                # Yavaşlama aşaması
                self.motor_values[idx] += step
                self.update_label(idx)
                deceleration_steps -= 1

            # Hedefe ulaşılmadıysa hareketi devam ettir
            if acceleration_steps + constant_speed_steps + deceleration_steps > 0:
                self.go_to_job_ids[idx] = self.root.after(100,
                                                          lambda idx=idx, target=target_position: self.go_to_position(
                                                              idx, target_position))
        else:
            # Motor hedef konumuna ulaştı, işlemi durdur
            if self.go_to_job_ids[idx] is not None:
                self.root.after_cancel(self.go_to_job_ids[idx])
                self.go_to_job_ids[idx] = None
            self.update_label(idx)

    def go_to_home(self):
        for i in range(len(self.motor_values)):
            self.go_to_position(i, target_position=0)

    def go_to_park(self):
        target_positions = [50, 100, 70, -81, 90, 10]
        for i in range(len(self.motor_values)):
            self.go_to_position(i, target_position=target_positions[i])

    def update_label(self, idx):
        self.motor_control.labels[idx].config(text=f" {self.motor_values[idx]}")


if __name__ == "__main__":
    robot_control = RobotControl(num_motors=6)
