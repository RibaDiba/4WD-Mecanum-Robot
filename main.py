import array, time
import neopixel
import os
import board
import busio
import micropython
import microcontroller
from pwmio import PWMOut
import digitalio
import pwmio
from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_ht16k33 import matrix


Dir_forward = 1
Dir_backward = -1


LF_forward = 1
LF_backward = -1

LB_forward = 1
LB_backward = -1

RF_forward = 1
RF_backward = -1

RB_forward = 1
RB_backward = -1

Adjustment = 1

Motor_LF_PWM = PWMOut(board.GP12)
Motor_LF_Dir = digitalio.DigitalInOut(board.GP13)
Motor_LF_Dir.direction = digitalio.Direction.OUTPUT

Motor_RF_PWM = PWMOut(board.GP15)
Motor_RF_Dir = digitalio.DigitalInOut(board.GP14)
Motor_RF_Dir.direction = digitalio.Direction.OUTPUT

Motor_RB_PWM = PWMOut(board.GP16)
Motor_RB_Dir = digitalio.DigitalInOut(board.GP17)
Motor_RB_Dir.direction = digitalio.Direction.OUTPUT

Motor_LB_PWM = PWMOut(board.GP19)
Motor_LB_Dir = digitalio.DigitalInOut(board.GP18)
Motor_LB_Dir.direction = digitalio.Direction.OUTPUT

def map(x,in_max, in_min, out_max, out_min):
    return (x - in_min)/(in_max - in_min)*(out_max - out_min) + out_min



class Motor():
    def __init__(self):
        pass

    def motor_left_front(self, status, direction, speed):
        if status == 0: # stop.
            Motor_LF_Dir.value = False
            Motor_LF_PWM.duty_cycle = 0
        else:
            value = int(map(speed, 100, 0, 65535, 0))

            if direction == Dir_forward:
                Motor_LF_Dir.value = False
                Motor_LF_PWM.duty_cycle = value
            elif direction == Dir_backward:
                Motor_LF_Dir.value = True
                Motor_LF_PWM.duty_cycle = 65535 - value

    def motor_right_front(self, status, direction, speed):
        if status == 0: # stop.
            Motor_RF_Dir.value = False
            Motor_RF_PWM.duty_cycle = 0
        else:
            value = int(map(speed,100,0,65535,0))

            if direction == Dir_forward:
                Motor_RF_Dir.value = False
                Motor_RF_PWM.duty_cycle = value
            elif direction == Dir_backward:
                Motor_RF_Dir.value = True
                Motor_RF_PWM.duty_cycle = 65535 - value

    # Control the M3 motor (right back).
    def motor_right_back(self, status, direction, speed):
        if status == 0: # stop.
            Motor_RB_Dir.value = False
            Motor_RB_PWM.duty_cycle = 0
        else:
            value = int(map(speed,100,0,65535,0))

            if direction == Dir_forward:
                Motor_RB_Dir.value = False
                Motor_RB_PWM.duty_cycle = value
            elif direction == Dir_backward:
                Motor_RB_Dir.value = True
                Motor_RB_PWM.duty_cycle = 65535 - value

    # Control the M4 motor (left back).
    def motor_left_back(self, status, direction, speed):
        if status == 0: # stop.
            Motor_LB_Dir.value = False
            Motor_LB_PWM.duty_cycle = 0
        else:
            value = int(map(speed,100,0,65535,0))

            if direction == Dir_forward:
                Motor_LB_Dir.value = False
                Motor_LB_PWM.duty_cycle = value
            elif direction == Dir_backward:
                Motor_LB_Dir.value = True
                Motor_LB_PWM.duty_cycle = 65535 - value


    def motor_stop(self):

            Motor_LF_Dir.value = False
            Motor_LF_PWM.duty_cycle = 0
            Motor_LB_Dir.value = False
            Motor_LB_PWM.duty_cycle = 0
            Motor_RF_Dir.value = False
            Motor_RF_PWM.duty_cycle = 0
            Motor_RB_Dir.value = False
            Motor_RB_PWM.duty_cycle = 0

    def move(self, status, direction, speed):
        if status == 0:
            self.motor_stop()
        else:
            if direction == "forward":
                print('forward')
                self.motor_left_front(1, LF_forward, speed)   # M1
                self.motor_right_front(1, RF_forward, speed)  # M2
                self.motor_right_back(1, RB_backward, speed)   # M3
                self.motor_left_back(1, LB_backward, speed)    # M4

            elif direction == "backward":
                print('backward')
                self.motor_left_front(1, LF_backward, speed)   # M1
                self.motor_right_front(1, RF_backward, speed)  # M2
                self.motor_right_back(1, RB_forward, speed)   # M3
                self.motor_left_back(1, LB_forward, speed)    # M4

            elif direction == "left":
                print('left')
                self.motor_left_front(1, LF_backward, speed)   # M1
                self.motor_right_front(1, RF_forward, speed)   # M2
                self.motor_right_back(1, RB_backward, speed)   # M3
                self.motor_left_back(1, LB_forward, speed)     # M4
            elif direction == "right":
                print('right')
                self.motor_left_front(1, LF_forward, speed)    # M1
                self.motor_right_front(1, RF_backward, speed)  # M2
                self.motor_right_back(1, RB_forward, speed)    # M3
                self.motor_left_back(1, LB_backward, speed)    # M4

            elif direction == "left_forward":
                print('left_forward')
                self.motor_left_front(1, LF_forward, speed)       # M1
                self.motor_right_front(0, RF_forward, speed*0.5)  # M2
                self.motor_right_back(1, RB_backward, speed)       # M3
                self.motor_left_back(0, LB_forward, speed*0.5)    # M4

            elif direction == "right_forward":
                print('right_forward')
                self.motor_left_front(0, LF_forward, speed*0.5)   # M1
                self.motor_right_front(1, RF_forward, speed)      # M2
                self.motor_right_back(0, RB_forward, speed*0.5)   # M3
                self.motor_left_back(1, LB_backward, speed)        # M4

            elif direction == "left_backward":
                print('left_backward')
                self.motor_left_front(0, LF_backward, speed*0.5)   # M1
                self.motor_right_front(1, RF_backward, speed)      # M2
                self.motor_right_back(0, RB_backward, speed*0.5)   # M3
                self.motor_left_back(1, LB_forward, speed)        # M4

            elif direction == "right_backward":
                print('right_backward')
                self.motor_left_front(1, LF_backward, speed)       # M1
                self.motor_right_front(0, RF_backward, speed*0.5)  # M2
                self.motor_right_back(1, RB_forward, speed)       # M3
                self.motor_left_back(0, LB_backward, speed*0.5)    # M4

            elif direction == "turn_left":
                print('turn_left')
                self.motor_left_front(1, LF_backward, speed)   # M1
                self.motor_right_front(1, RF_forward, speed)   # M2
                self.motor_right_back(1, RB_forward, speed)    # M3
                self.motor_left_back(1, LB_backward, speed)    # M4

            elif direction == "turn_right":
                print('turn_right')
                self.motor_left_front(1, LF_forward, speed)     # M1
                self.motor_right_front(1, RF_backward, speed)   # M2
                self.motor_right_back(1, RB_backward, speed)    # M3
                self.motor_left_back(1, LB_forward, speed)      # M4
            else:
                print("Direction error!")



class IR(object):

    CODE = {162: "1", 98: "2", 226: "3", 34: "4", 2: "5", 194: "6", 224: "7", 168: "8", 144: "9",
            152: "0", 104: "*", 176: "#", 24: "up", 74: "down", 16: "left", 90: "right", 56: "ok"}

    def __init__(self, gpioNum):
        self.irRecv = digitalio.DigitalInOut(gpioNum)
        self.irRecv.direction = digitalio.Direction.INPUT
        self.irRecv.pull = digitalio.Pull.UP

        self.ir_step = 0
        self.ir_count = 0
        self.buf64 = [0 for i in range(64)]
        self.recived_ok = False
        self.cmd = None
        self.cmd_last = None
        self.repeat = 0
        self.repeat_last = None
        self.t_ok = None
        self.t_ok_last = None
        self.start = 0
        self.start_last = 0
        self.changed = False
        self.prev = True

    def __logHandler(self, rise):
        thisComeInTime = time.monotonic_ns()

        # update time
        curtime = time.monotonic_ns() - self.start
        self.start = thisComeInTime

        if curtime >= 8500*1000 and curtime <= 9500*1000:
            self.ir_step = 1
            return

        if self.ir_step == 1:
            if curtime >= 4000*1000 and curtime <= 5000*1000:
                self.ir_step = 2
                self.recived_ok = False
                self.ir_count = 0
                self.repeat = 0
            elif curtime >= 2000*1000 and curtime <= 3000*1000:  # Long press to repeat
                self.ir_step = 3
                self.ir_step += 1
                self.repeat += 1

        elif self.ir_step == 2:  # receive 4 bytes
            self.buf64[self.ir_count] = curtime
            self.ir_count += 1
            if self.ir_count >= 64:
                self.recived_ok = True
                self.t_ok = self.start #Record the last ok time
                self.ir_step = 0

        elif self.ir_step >= 3:  # repeat
            self.repeat = 0



    def __check_cmd(self):
        byte4 = 0
        for i in range(32):
            x = i * 2
            t = self.buf64[x] + self.buf64[x+1]
            byte4 <<= 1
            if t >= 1800*1000 and t <= 2800*1000:
                byte4 += 1
        user_code_hi = (byte4 & 0xff000000) >> 24
        user_code_lo = (byte4 & 0x00ff0000) >> 16
        data_code = (byte4 & 0x0000ff00) >> 8
        data_code_r = byte4 & 0x000000ff
        self.cmd = data_code

    def __check_edge(self, prev, cur):
        if prev == True and cur == False:
            return 'falling'
        elif prev == False and cur == True:
            return 'rising'
        else:
            return 'none'

    def scan(self):
        # check edge
        cur = self.irRecv.value
        edge = self.__check_edge(self.prev, cur)
        self.prev = cur
        # simulate interrupt
        if edge == 'rising':
            self.__logHandler(True)
        elif edge == 'falling':
            self.__logHandler(False)

        # data received
        if self.recived_ok:
            self.__check_cmd()
            self.recived_ok = False

        # data has changed()
        if self.cmd != self.cmd_last or self.repeat != self.repeat_last or self.t_ok != self.t_ok_last:
            self.changed = True
        else:
            self.changed = False

        # renew
        self.cmd_last = self.cmd
        self.repeat_last = self.repeat
        self.t_ok_last = self.t_ok
        # Corresponding button character
        s = self.CODE.get(self.cmd)
        return self.changed, s, self.repeat, self.t_ok

