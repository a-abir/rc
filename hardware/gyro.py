from ctre import PigeonIMU as Pigeon


class Gyro:
    CAN_ID = 10
    offset = 0

    def __init__(self):
        self.pigeon = Pigeon(self.CAN_ID)
        self.reset()

    def reset(self):
        self.offset += self.getAngle()

    def getAngle(self):
        return self.getGyroData()[2] - self.offset

    def getGyroData(self):
        try:
            return self.pigeon.getAccumGyro()
        except:
            return (0, 0, 0)