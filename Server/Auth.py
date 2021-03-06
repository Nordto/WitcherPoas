from Server.Objects import User
from Server.Objects import Object
from Server.Objects import Status
from enum import Enum
from hashlib import md5
import time


class EventAuth(Enum):
    SuccessAuthorizaion = "Success"
    LoginNotExist = "LoginNotExist"
    PasswordIncorrect = "IncorrectPasswd"


def authorization(cursor, params):
    cursor.execute("select * from Authorization_info where login='{}'".format(params[User.Login.value]))
    row = cursor.fetchone()

    status = Object()
    obj = Object()
    status.status = Status.Error.value

    if row is None:
        obj.message = EventAuth.LoginNotExist.value
    elif row[2] == params[User.Password.value]:
        obj.message = EventAuth.SuccessAuthorizaion.value
        status.status = Status.Ok.value
        tok = params[User.Login.value] + time.time().__str__()
        obj.token = md5(tok.encode('utf-8')).hexdigest()
        cursor.execute("insert into Token_Table (token, last_update) values('{}', {})".format(obj.token, time.time().__int__()))
    else:
        obj.message = EventAuth.PasswordIncorrect.value

    status.object = obj
    return status.toJSON()

def authUser(cursor, params):
    cursor.execute("select * from Token_Table where token='{}'".format(params[User.Token.value]))
    row = cursor.fetchone()
    return row is not None
