# Microservice1-User-Service

This microservice is a fundamental component of our application, responsible for managing all user-related functionalities. It handles authentication, authorization, and user profile management for both general users and restaurant owners. The User Microservice is built using Django. It operates independently with its own database and exposes a set of RESTful API endpoints for integration with the composite microservice and other sub-microservices.## Features

## Features
- **User Authentication and Authorization**
- **Profile Management**
- **Support for Multiple User Roles**
- **RESTful API Endpoints**

## API Endpoints

### Base Message
- ```GET /```
  Returns a welcome message or basic information about the microservice.
### Add User
- ```POST /add_user/```
  Creates a new user account. Expects user data in JSON format in the request body.
### Get All Users
- ```GET /get_all_users/```
  Retrieves a list of all registered users.
### Delete User
- ```DELETE /delete-user/<int:uni>/```
  Deletes a user account specified by user's uni.
  
