import os
import time
import board
import digitalio
import pwmio


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
                self.repeat += 1

        elif self.ir_step == 2:  # receive 4 bytes
            self.buf64[self.ir_count] = curtime
            self.ir_count += 1
            if self.ir_count >= 64:
                self.recived_ok = True
                self.t_ok = self.start #Record the last ok time
                self.ir_step = 0

        elif self.ir_step == 3:  # repeat
            if curtime >= 500*1000 and curtime <= 650*1000:
                self.repeat += 1

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
