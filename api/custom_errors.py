import os
from api import response_status

class CustomErrors(Exception):
    message = ""
    status = 0

    def __init__(self, message, status):
        self.message = message
        self.status = status
        #Just for log (actually in console)
        print (message)

    @staticmethod
    def NotFound(mesage):
        return CustomErrors(mesage, response_status.STATUS_NOT_FOUND)

    @staticmethod
    def InternalServer(mesage):
        return CustomErrors(mesage, response_status.STATUS_INTERNAL_ERROR)

    @staticmethod
    def Unauthorized():
        return CustomErrors("You shall not pass", response_status.STATUS_UNAUTHORIZED)
