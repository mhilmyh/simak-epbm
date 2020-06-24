from model import Robot
import config


def autoEPBM():
    robot = Robot(config.USERNAME_IPB, config.PASSWORD_IPB)
    robot.login()
    robot.login(method='POST')


if __name__ == '__main__':
    autoEPBM()
