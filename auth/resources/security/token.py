import json
import base64

from datetime import datetime
from Crypto.Cipher import AES

from schemas import TokenEmail
from settings import config


class PasswordResetTokenGenerator:
    """
    Strategy object used to generate and check tokens for the password
    reset mechanism.
    """
    def __init__(self):
        self._secret_key = base64.b64encode(bytes(config.SECRET_KEY, 'utf-8'))[64:]

    def crypto_encode(self, user_id: int):
        encryption_cipher = AES.new(self._secret_key, AES.MODE_OPENPGP)
        ciphertext = encryption_cipher.encrypt(self._make_body(user_id))
        b64_ciphertext = base64.b64encode(ciphertext).decode()
        return b64_ciphertext

    def crypto_decode(self, token: str):
        unb64_ciphertext = base64.b64decode(bytes(token.replace(' ', '+'), 'utf-8'))
        iv = unb64_ciphertext[0:18]
        unb64_ciphertext = unb64_ciphertext[18:]
        decryption_cipher = AES.new(self._secret_key, AES.MODE_OPENPGP, iv=iv)

        _data_in_token = TokenEmail(**json.loads(decryption_cipher.decrypt(unb64_ciphertext).decode('utf-8')))
        if self._verify_token(data=_data_in_token):
            return _data_in_token.id

    @staticmethod
    def _make_body(user_id: int) -> bytes:
        _data_to_string = TokenEmail(id=user_id).json()
        return bytes(_data_to_string, 'utf-8')

    @staticmethod
    def _verify_token(data):
        _delta_time = datetime.now().timestamp() - data.timestamp
        if _delta_time > config.TOKEN_LIVE_TIME:
            return False
        return True


token_manager = PasswordResetTokenGenerator()
