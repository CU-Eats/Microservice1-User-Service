# Microservice1-User-Service

This microservice is a fundamental component of our application, responsible for managing all user-related functionalities. It handles authentication, authorization, and user profile management for both general users and restaurant owners. The User Microservice is built using Django. It operates independently with its own database and exposes a set of RESTful API endpoints for integration with the composite microservice and other sub-microservices.## Features

## Features
- **User Authentication and Authorization**
- **Profile Management**
- **Support for Multiple User Roles**
- **RESTful API Endpoints**

## API Endpoints

### Base Message
- URL: ```GET /```
- Description: Returns a welcome message or basic information about the microservice.
- Input argument: None
  
### Add User
- URL: ```POST /add_user/```
- Description: Creates a new user account. Expects user data in JSON format in the request body.
- Input argument:
  | Parameter    | Type    |  Description                                     |
  |--------------|---------| -------------------------------------------------|
  | `uni`        | Integer | Unique numeric identifier for the user          |
  | `email`      | String  | Email address of the user                       |
  | `first_name` | String  | First name of the user                          |
  | `last_name`  | String  | Last name of the user                           |
  | `id_type`    | String  | Type of user ID (`student`, `faculty`, `guest`) |
  | `password`   | String  | Password for the user account                   |

  
### Get All Users
- URL: ```GET /get_all_users/```
- Description: Retrieves a list of all registered users.
- Input argument: None
  
### Delete User
- URL: ```DELETE /delete-user/<int:uni>/```
- Description: Deletes a user account specified by user's uni.
- Input argument:
  | Parameter | Type    |  Description                            |
  | --------- | ------- |  -------------------------------------- |
  | uni       | Integer |  Unique numeric identifier of the user  |


### Check User Password:
- URL: ```GET /get_one_user/```
- Description: Verify if the input uni and password match to the user account.
- Input argument: uni, password
  
