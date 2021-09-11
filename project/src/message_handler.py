from typing import Union, Dict


class MessageHandler:
    SUCCESS_CODE = 0
    ERROR_CODE = 1
    
    @classmethod
    def get_success_msg(cls, message: str) -> Dict[str, Union[str, int]]:
        return {"msg": message, "exit_code": cls.SUCCESS_CODE}

    @classmethod
    def get_error_msg(cls, error_msg: str) -> Dict[str, Union[str, int]]:
        return {"error": error_msg, "exit_code": cls.ERROR_CODE}
