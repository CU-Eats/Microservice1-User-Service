from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import users
from .serializer import UserSerializer

@api_view(['GET'])
def base_message(request):
    return Response({"message": "Welcome to the User API!"})

@api_view(['POST'])
def add_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_user(request, uni):
    try:
        user_item = users.objects.get(uni=uni)
    except users.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    user_item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_all_users(request):
    all_users = users.objects.all()
    serializer = UserSerializer(all_users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
