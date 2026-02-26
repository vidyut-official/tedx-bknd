


from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import IntegrityError,transaction

from ..models import User

class RegisterUser(APIView):

    def post(self,request):
        username = request.data.get("username")
        email = request.data.get("email")




        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username = request.data.get("username"),
                    email = request.data.get("email"),
                    password = request.data.get("password"),
                    user_type = request.data.get("user_type"),
                    user_role = request.data.get("user_role"),
                )

                return Response({
                    "response" : "User created successfully"
                },status=200)
            

            
        except KeyError as e:
            return Response(
                {
                    "error" : f"Missing field: {str(e)}"
                },status=400
            )
        except IntegrityError:
            return Response(
                {
                    "error" : "User already exists"
                },status=409
            )
        except Exception:
            return Response(
                {
                    "error" : "Something went wrong, try again"
                },status=500
            )


        
