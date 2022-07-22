from typing import List, Optional
from fastapi import Request

class UserCreateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get("username")
        self.password = form.get("username")

    async def is_valid(self):
        if not self.username or not len(self.username) > 5:
            self.errors.append("Username should be more than 5 chars")
        if not self.password or not len(self.password) >= 6:
            self.errors.append("Password must be more than 6 chars")
        if not self.errors:
            return True
        return False
