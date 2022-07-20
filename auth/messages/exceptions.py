from fastapi import HTTPException


class Exceptions:

    @property
    def authenticate_not_header(self) -> HTTPException:
        return HTTPException(
            status_code=401,
            detail='Not Authenticate token',
            headers={'WWW-Authenticate': 'Token'},
        )

    @property
    def credential_not_correct(self) -> HTTPException:
        return HTTPException(
            status_code=401,
            detail='Incorrect username or password',
        )

    @property
    def authorization_header_token(self) -> HTTPException:
        return HTTPException(
            status_code=401,
            detail='Format Headers -> Authorization: Token <your_token_from_login> ',
            headers={'WWW-Authenticate': 'Token'},
        )

    @property
    def logged_in(self):
        return HTTPException(
            status_code=401,
            detail='User already logged in',
            headers={'WWW-Authenticate': 'Token'},
        )

    @property
    def session_not_correct(self):
        return HTTPException(
            status_code=403,
            detail="Invalid session"
        )

    @property
    def password_match_not_valid(self):
        return HTTPException(
            status_code=400,
            detail='Passwords do not match'
        )

    @property
    def token_email_not_valid(self):
        return HTTPException(
            status_code=400,
            detail='Token not valid'
        )

    @property
    def email_not_valid(self):
        return HTTPException(
            status_code=400,
            detail='Not valid format email'
        )

    @property
    def session_black_list(self):
        return HTTPException(
            status_code=403,
            detail='Session in black list'
        )

    @property
    def not_create_user(self):
        return HTTPException(
            status_code=403,
            detail='Can`t not create user'
        )

    @property
    def not_is_verified(self):
        return HTTPException(
            status_code=403,
            detail='Not verified'
        )

    @property
    def google_login_error(self):
        return HTTPException(
            status_code=403,
            detail='Not connect Google'
        )

    @property
    def facebook_login_error(self):
        return HTTPException(
            status_code=403,
            detail='Not connect Google'
        )

    @property
    def not_valid_provider(self):
        return HTTPException(
            status_code=400,
            detail='Not valid provider'
        )

    @property
    def email_provider(self):
        return HTTPException(
            status_code=400,
            detail='If you are using a provider email you need to use the fields, email and password'
        )
