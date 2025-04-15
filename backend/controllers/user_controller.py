from database.model.models import User

class UserController:
    def __init__(self, sql_controller):
        self.sql_controller = sql_controller

    async def upsert_user(self, login_request):
        user_payload = {
            "Email": login_request.Email,
            "FirstName": login_request.FirstName,
            "LastName": login_request.LastName,
            "StudentID": login_request.StudentID,
        }
        if hasattr(login_request, 'School') and login_request.School:
            user_payload["School"] = login_request.School
        if hasattr(login_request, 'ClassLevel') and login_request.ClassLevel:
            user_payload["ClassLevel"] = login_request.ClassLevel

        existing_user = await self.sql_controller.get_user(login_request.Email)
        if existing_user:
            update_fields = {}
            if existing_user.School is None and login_request.School:
                update_fields["School"] = login_request.School
            if existing_user.ClassLevel is None and login_request.ClassLevel:
                update_fields["ClassLevel"] = login_request.ClassLevel
            if update_fields:
                await self.sql_controller.update_user(login_request.Email, **update_fields)
        else:
            await self.sql_controller.insert_user(User(**user_payload))