from main import Motor, IR
import board
import time

motor = Motor()
pin = board.GP22
ir = IR(pin)

info = ''
' '
speed = 50
# Infrared reception interval time.
IR_delay_time = 0.11



def IR_move():

    while True:
        result = []
        changed, button, repeat, t_ok = ir.scan()
        if changed:

            # Perform actions when a new infrared signal is received
            result = [button, repeat, t_ok]  # Write button, repeat, t_ok to the list
            print("Command: %s" %result[0])
            #time.sleep(0.01)

            if(result[0]!=None):
                if result[0] == "up":
                    motor.move(1, "forward", speed)
                    time.sleep(0.2)
                    motor.motor_stop()
                elif result[0] == "down":
                    motor.move(1, "backward", speed)
                    time.sleep(0.2)
                    motor.motor_stop()
                elif result[0] == "left":
                    motor.move(1, "left", speed)
                    time.sleep(0.2)
                    motor.motor_stop()
                elif result[0] == "right":
                    motor.move(1, "right", speed)
                    time.sleep(0.2)
                    motor.motor_stop()
                elif result[0] == "1":
                    motor.move(1, "left_forward", speed)
                    time.sleep(0.2)
                    motor.motor_stop()
                elif result[0] == "3":
                    motor.move(1, "right_forward", speed)
                    time.sleep(0.2)
                    motor.motor_stop()
                elif result[0] == "7":
                    motor.move(1, "left_backward", speed)
                    time.sleep(0.2)
                    motor.motor_stop()
                elif result[0] == "9":
                    motor.move(1, "right_backward", speed)
                    time.sleep(0.2)
                    motor.motor_stop()
                elif result[0] == "4":
                    motor.move(1, "turn_left", speed)
                    time.sleep(0.2)
                    motor.motor_stop()
                elif result[0] == "6":
                    motor.move(1, "turn_right", speed)
                    time.sleep(0.2)
                    motor.motor_stop()
                else:
                    pass