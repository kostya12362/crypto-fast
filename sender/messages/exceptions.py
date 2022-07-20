from fastapi import HTTPException


class Exceptions:

    @property
    def not_valid_to_emails(self) -> HTTPException:
        return HTTPException(
            detail="Not valid 'to_emails'",
            status_code=400
        )

    @property
    def not_valid_to_phone(self) -> HTTPException:
        return HTTPException(
            detail="Not valid mobile number",
            status_code=400
        )
