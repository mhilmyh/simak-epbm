from model import Robot
import config


def autoEPBM(username=None, password=None):
    if username is None and password is None:
        robot = Robot(config.USERNAME_IPB, config.PASSWORD_IPB)
        robot.login()
        robot.login(method='POST_LOGIN')
        robot.list_sidebar()
        # robot.goto_page(page_name='EPBM')
    else:
        raise ValueError('Cek kembali username dan password yang diberikan')


if __name__ == '__main__':
    autoEPBM()
