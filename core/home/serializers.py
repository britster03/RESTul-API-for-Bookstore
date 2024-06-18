from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
       # field=['name']
        fields =['name']
        
    def validate(self,data):
        if data['name']:
            for n in data['name']:
                if n.isdigit():
                    raise serializers.ValidationError({'error':'names cannot be numeric'})
                
        return data
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
       # field=['name']
        fields ='__all__'

class BookSerializer(serializers.ModelSerializer):
    category=CategorySerializer()
    class Meta:
        model = Book
       # field=['name']
        fields ='__all__'