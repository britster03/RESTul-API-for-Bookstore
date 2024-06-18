import datetime
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import *
from .views import *
from .helpers import *
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated



@api_view(['GET'])
def get_book(request):
    book_objs = Book.objects.all()
    serializer = BookSerializer(book_objs, many = True)
    return Response({'status': 200, 'payload':serializer.data})


from rest_framework import generics
class StudentGeneric(generics.ListAPIView,generics.CreateAPIView):
    queryset=Student.objects.all()
    serializer_class=StudentSerializer

class StudentGeneric1(generics.UpdateAPIView , generics.DestroyAPIView):
    queryset=Student.objects.all()
    serializer_class=StudentSerializer
    lookup_field='id'
    
from rest_framework_simplejwt.tokens import RefreshToken

class GeneratePDF(APIView):
    def get(self, request):
        student_objs = Student.objects.all()
        params= {
            'today':datetime.date.today(),
            'student_objs': student_objs
        }
        file_name , status = save_pdf(params)
        
        if not status:
            return Response({'status':404})
        
        return Response({'status':200, 'path': f'/media/{file_name}.pdf'})

class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data =request.data)
            
        if not serializer.is_valid():
            return Response({'status': 403,'error': serializer.errors,'message':'something went wrong'})
    
        serializer.save()
        user = User.objects.get(username = serializer.data['username'])
        refresh = RefreshToken.for_user(user)

# Create your views here.

        return Response({'status': 200, 'payload':serializer.data,'refresh': str(refresh),
        'access': str(refresh.access_token), 'message':'you sent'})

class StudentAPI(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self, request):
            student_objs = Student.objects.all()
            serializer = StudentSerializer(student_objs, many = True)
            return Response({'status': 200, 'payload':serializer.data})
        
    def post(self, request):
        data = request.data
        serializer = StudentSerializer(data=request.data)
    
        if not serializer.is_valid():
            return Response({'status': 403,'error': serializer.errors,'message':'something went wrong'})
    
        serializer.save()
# Create your views here.

        return Response({'status': 200, 'payload':serializer.data,'message':'you sent'})
    
    def put(self, request):
        try:
            student_obj = Student.objects.get(id=request.data['id'])
            serializer = StudentSerializer(student_obj,data=request.data,partial=True)
    
            if not serializer.is_valid():
                return Response({'status': 403,'error': serializer.errors,'message':'something went wrong'})
    
            serializer.save()
            return Response({'status': 200, 'payload':serializer.data,'message':'you sent'})
# Create your views here.

        except Exception as e:
            print(e)
        return Response({'status':201,'message':'invalid id'})
        
    def patch(self, request):
        pass
    
    def delete(self, request):
        try:
            id=request.GET.get('id')
            student_obj = Student.objects.get(id=id)
            student_obj.delete()
            return Response({'status': 403,'message':'deleted'})
    

# Create your views here.

        except Exception as e:
            print(e)
        return Response({'status':201,'message':'invalid id'})

