from model import Robot
import config


def autoEPBM(username=None, password=None):
    if username is None and password is None:
        robot = Robot(config.USERNAME_IPB, config.PASSWORD_IPB)
    elif username is not None and password is not None:
        robot = Robot(username, password)
    else:
        raise ValueError(
            '\033[31mCek kembali username dan password yang diberikan\33[0m')

    robot.login()
    robot.login(method='POST_LOGIN')
    robot.sidebar()
    robot.goto_page(page_name='EPBM')
    for epbm in robot.get_list_epbm().keys():
        robot.fill_epbm(epbm)


if __name__ == '__main__':
    autoEPBM()
