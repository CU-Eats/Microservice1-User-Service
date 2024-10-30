from django.http import Http404
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
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
    request_data = request.data.copy()
    if "password" in request_data:
        request_data["password"] = make_password(request_data["password"])
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

@api_view(['GET'])
def check_user_password(request):
    user_id = request.query_params.get("uni")
    password = request.query_params.get("password")

    # Check if both parameters are provided
    if not user_id or not password:
        return Response({"error": "Please provide both 'id' and 'password' parameters."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Narrow down by id
        user = users.objects.get(uni=user_id)

        # Check if password matches
        if check_password(password, user.password):
            return Response({"message": "Password is correct."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Password is incorrect."}, status=status.HTTP_401_UNAUTHORIZED)

    except users.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
