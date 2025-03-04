import re
import asyncio
from metagpt.actions import Action
from metagpt.roles import Role
from metagpt.schema import Message
from metagpt.logs import logger

import os

import rtde_control
import rtde_receive
import math
import serial
import time

# 设置代理环境变量
os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

# 之后的代码可以使用这些代理设置进行网络请求


OriginPoint = [90.00, -90.00, -90.00, -90.00, 90.00, 0.00]
# Point00 = [118.90, -106.99, -109.46, -53.64, 90.08, 28.87]  # -161.93, 520.96, -219.52, 3.140, 0.000, 0.000
# Point0X为抓取点
Point01 = [127.44, -110.70, -102.15, -57.10, 89.94, 37.38]  # -261.68, 523.27, -207.95, 3.140, 0.000, 0.000
Point02 = [108.78, -103.77, -111.77, -54.37, 89.97, 18.75]  # -61.68, 523.25, -207.88, 3.140, 0.000, 0.000
Point03 = [86.93, -105.49, -109.48, -54.92, 90.01, -3.11]  # 138.27, 523.20, -207.90, 3.140, 0.000, 0.000
Point04 = [67.32, -115.17, -95.46, -59.25, 90.06, -22.77]  # 338.25, 523.21, -207.91, 3.140, 0.000, 0.000
# Point0X_300为接近点
Point04_300 = [67.28, -107.21, -77.53, -85.33, 89.98, -22.84]  # 338.11, 520.99, -19.48, 3.140, 0.000, 0.000
Point03_300 = [86.95, -95.94, -91.26, -82.88, 90.00, -3.12]  # 138.12, 520.99, -19.48, 3.140, 0.000, 0.000
Point02_300 = [108.89, -93.98, -93.39, -82.71, 90.03, 18.82]  # -61.88, 521.01, -19.40, 3.140, 0.000, 0.000
Point01_300 = [127.59, -101.97, -84.20, -83.92, 90.06, 37.50]  # -261.86, 521.02, -19.42, 3.140, 0.000, 0.000


# 假设`ur_control`是已经定义好的对象实例
# 这里是模拟的`ur_control`对象及其方法，实际使用时应替换为真实对象
class GripperControl:
    def __init__(self, port='/dev/ttyUSB0', baud_rate=115200):
        # '/dev/ttyUSB0' COM3
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
    def __init__(self, robot_ip="192.168.2.100", gripper_port='/dev/ttyUSB0', gripper_baud_rate=115200):
        self.robot_ip = robot_ip
        # self.rtde_c = rtde_control.RTDEControlInterface(robot_ip)
        self.rtde_c = rtde_control.RTDEControlInterface(self.robot_ip)
        self.rtde_r = rtde_receive.RTDEReceiveInterface(self.robot_ip)
        self.gripper_control = GripperControl(gripper_port, gripper_baud_rate)

    @staticmethod
    def degrees_to_radians(angle_array):
        return [math.radians(angle) for angle in angle_array]

    def move_to_position1(self):
        self.rtde_c.moveJ(self.degrees_to_radians(Point01_300))
        self.rtde_c.moveJ(self.degrees_to_radians(Point01))

    def move_to_position2(self):
        self.rtde_c.moveJ(self.degrees_to_radians(Point02_300))
        self.rtde_c.moveJ(self.degrees_to_radians(Point02))

    def move_to_position3(self):
        self.rtde_c.moveJ(self.degrees_to_radians(Point03_300))
        self.rtde_c.moveJ(self.degrees_to_radians(Point03))

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


class URControlCode(Action):
    PROMPT_TEMPLATE: str = """
        现在需要机械手去位置1夹取物体，然后移动到位置2放置物体。再去位置2夹取物体，移动到位置3。
        请写一下机械手需要执行的步骤，一步步思考过程的正确性，然后将代码写在下面的代码框中。不要有其他无关文字，直接给出调用函数
        参考函数如下：
        {instruction}
        返回```步骤1:xxx
        步骤2:xxx
        步骤3:xxx
        ....
        ```，不要有其他文字。
        参考案例如下：'''
        步骤1: ur_control.move_to_position1()
        步骤2: ur_control.gripper_control.close_gripper()
        步骤3: ur_control.move_to_position2()
        步骤4: ur_control.gripper_control.open_gripper()
        步骤5: ur_control.move_to_position2()
        步骤6: ur_control.gripper_control.close_gripper()
        步骤7: ur_control.move_to_position3()
        步骤8: ur_control.gripper_control.open_gripper()
        '''
        你的执行步骤：

        """

    name: str = "URControlCode"

    async def run(self, instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)
        rsp = await self._aask(prompt)
        # print(rsp)
        extracted_codes = URControlCode.parse_code(rsp)
        # print(extracted_codes)
        return extracted_codes

    @staticmethod
    def parse_code(rsp):
        # 提取Python代码
        # 假设有效代码行都是以"ur_control"开头
        extracted_codes = re.findall(r'ur_control[^\n]+', rsp)
        return extracted_codes


class URcontrol(Role):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([URControlCode])

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: ready to {self.rc.todo}")
        todo = self.rc.todo  # todo will be SimpleWriteCode()

        msg = self.get_memories(k=1)[0]  # find the most recent messages

        # print(f"msg:{msg}")
        extracted_codes = await todo.run(msg.content)
        msg = Message(content=msg.content, role=self.profile,
                      cause_by=type(todo))

        return extracted_codes


async def main():
    msg = '''使用move_to_initial_position方法将机器人移动到初始位置。传递一个角度数组，表示机器人各关节的目标位置（度）。
input_angles = [20.00 - 90.00, -90.00, -90.00, -90.00, 0.00]  # 替换为你的目标角度
ur_control.move_to_initial_position(input_angles)
控制夹爪
使用gripper_control属性中的方法来初始化、打开或关闭夹爪。
初始化夹爪：
ur_control.gripper_control.init_gripper()
关闭夹爪：
ur_control.gripper_control.close_gripper()
打开夹爪：
ur_control.gripper_control.open_gripper()'''

    role = URcontrol()
    logger.info(msg)
    extracted_codes = await role.run(msg)
    logger.info(extracted_codes)

    robot_ip = "192.168.2.100"
    input_angles = [90.00, -90.00, -90.00, -90.00, 90.00, 0.00]
    ur_control = URControlLibrary(robot_ip, '/dev/ttyUSB0', 115200)
    ur_control.move_to_initial_position(input_angles)
    ur_control.gripper_control.init_gripper()
    # ur_control.gripper_control.close_gripper()
    ur_control.gripper_control.open_gripper()
    # 执行提取的代码
    for code in extracted_codes:
        exec(code)

    ur_control.move_to_initial_position(input_angles)


asyncio.run(main())
