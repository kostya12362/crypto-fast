from fastapi.responses import JSONResponse


class Details:

    @classmethod
    def message_to_email(cls, data) -> JSONResponse:
        return JSONResponse(
            content={"detail": f"Message sending to email {','.join(data.to_emails)}"}
        )

    @classmethod
    def message_to_phone(cls, data) -> JSONResponse:
        return JSONResponse(
            content={"detail": f"Message sending to phone {','.join(data.to_phones)}"}
        )
