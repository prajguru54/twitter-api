from fastapi import HTTPException, status


forbidden_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Not allowed to perform the specified operation",
)
