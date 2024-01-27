import bcrypt
from django.http import JsonResponse
from rest_framework.views import APIView

from ogame.models import Users

class testAPIView(APIView):
    def post(self, request):
        password = "Faischier1"
        password_bytes = bytes(password, 'utf-8')
        salt = bcrypt.gensalt()
        
        password_hashed = bcrypt.hashpw(password_bytes, salt)
        # hashed_password_bytes = bytes(password_hashed, 'utf-8')
        # print(password_hashed)
        Users.objects.filter(id=4).update(password=password_hashed.decode('utf-8'))
        # print(user.salt)
        user = Users.objects.filter(id=4).first()
        if bcrypt.checkpw(bytes('yeh/gldo', 'utf-8') , user.password.encode('utf-8')):
            print("It Matches!")
        return JsonResponse({'msg': 'Ressources ajoutées'})