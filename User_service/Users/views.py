from django.http import Http404
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import users
from .serializer import UserSerializer
import boto3
from botocore.exceptions import ClientError
from decouple import config

# Load AWS credentials and sender email from .env
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_REGION = config('AWS_REGION', default='us-east-2')
EMAIL_FROM = config('EMAIL_FROM')


# Function to send email using AWS SES
def send_account_creation_email(to_email, user_name):
    ses_client = boto3.client(
        'ses',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )

    subject = "Welcome to CU Eats!"

    # Email content
    html_body = f"""
    <html>
        <body>
            <h1>Hi {user_name},</h1>
            <p>Welcome to our CU Eats! Your account has been successfully created.</p>
            <p>We are excited to have you on board.</p>
            <p>Regards,<br>The Team</p>
        </body>
    </html>
    """

    text_body = f"""
    Hi {user_name},
    Welcome to our CU Eats! Your account has been successfully created.
    We are excited to have you on board.
    Regards,
    The Team
    """

    try:
        response = ses_client.send_email(
            Source=EMAIL_FROM,
            Destination={'ToAddresses': [to_email]},
            Message={
                'Subject': {'Data': subject},
                'Body': {
                    'Text': {'Data': text_body},
                    'Html': {'Data': html_body}
                }
            }
        )
        print(f"Email sent to {to_email}, Message ID: {response['MessageId']}")
    except ClientError as e:
        print(f"Failed to send email: {e.response['Error']['Message']}")
        raise e


# View functions
@api_view(['GET'])
def base_message(request):
    return Response({"message": "Welcome to the User API!"})


@api_view(['POST'])
def add_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        # Save the user to the database
        user = serializer.save()

        # Send email notification
        try:
            send_account_creation_email(
                to_email=user.email,
                user_name=user.first_name  # Assuming `first_name` is a field in your model
            )
        except Exception as e:
            return Response({"error": "User created but failed to send email.", "details": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        return Response({"error": "Please provide both 'id' and 'password' parameters."},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        # Narrow down by id
        user = users.objects.get(uni=user_id)

        # Check if password matches
        if password == user.password:
            user_info = {
                "uni": user.uni,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "id_type": user.id_type,
            }
            return Response({"message": "Password is correct.", "user_info": user_info}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Password is incorrect."}, status=status.HTTP_401_UNAUTHORIZED)

    except users.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
