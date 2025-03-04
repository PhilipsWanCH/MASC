import rtde_control
import math
import serial
import time


class GripperControl:
    def __init__(self, port='COM3', baud_rate=115200):
        self.port = port
        self.baud_rate = baud_rate
        self.ser = serial.Serial(port, baud_rate, timeout=1)

    def send_hex_command(self, hex_command):
        command_bytes = bytes.fromhex(hex_command)
        self.ser.write(command_bytes)
        time.sleep(0.1)
        response = self.ser.read(self.ser.inWaiting())
        return response

    def close_gripper(self):
        close_command = "0106010300007836"
        print("Sending close command...")
        response = self.send_hex_command(close_command)
        print("Response:", response.hex())
        time.sleep(1)

    def open_gripper(self):
        open_command = "0106010303E87888"
        print("Sending open command...")
        response = self.send_hex_command(open_command)
        print("Response:", response.hex())
        time.sleep(1)

    def init_gripper(self):
        init_command = "01060100000149F6"
        print("Sending init command...")
        response = self.send_hex_command(init_command)
        print("Response:", response.hex())
        time.sleep(1)

    def close(self):
        self.ser.close()


class URControlLibrary:
    def __init__(self, robot_ip, gripper_port='COM3', gripper_baud_rate=115200):
        self.robot_ip = robot_ip
        self.rtde_c = rtde_control.RTDEControlInterface(robot_ip)
        self.gripper_control = GripperControl(gripper_port, gripper_baud_rate)

    @staticmethod
    def degrees_to_radians(angle_array):
        return [math.radians(angle) for angle in angle_array]

    def move_to_initial_position(self, input_angles, velocity=0.5, acceleration=0.5):
        """
        Move to initial joint position with a regular moveJ.
        """
        radian_angles = self.degrees_to_radians(input_angles)
        self.rtde_c.moveJ(radian_angles, velocity, acceleration)

    def servo_control_loop(self, input_angles, velocity=0.5, acceleration=0.5, dt=1.0 / 125, lookahead_time=0.1,
                           gain=300, duration=2):
        """
        Execute control loop for a specified duration.
        """
        joint_q = self.degrees_to_radians(input_angles)
        for _ in range(int(duration / dt)):
            t_start = self.rtde_c.initPeriod()
            self.rtde_c.servoJ(joint_q, velocity, acceleration, dt, lookahead_time, gain)
            joint_q[4] += 0.001  # Modify as needed
            joint_q[5] += 0.001  # Modify as needed
            self.rtde_c.waitPeriod(t_start)

    def stop(self):
        """
        Stop the servo and the script.
        """
        self.rtde_c.servoStop()
        self.rtde_c.stopScript()


# Example usage
if __name__ == "__main__":
    robot_ip = "192.168.2.100"
    input_angles = [20.00 - 90.00, -90.00, -90.00, -90.00, 0.00]
    ur_control = URControlLibrary(robot_ip, 'COM3', 115200)
    ur_control.move_to_initial_position(input_angles)
    ur_control.gripper_control.init_gripper()
    ur_control.gripper_control.close_gripper()
    ur_control.gripper_control.open_gripper()
    ur_control.gripper_control.close()
    ur_control.stop()
