# Recipe Application Dashboard
What the application does at a high level?
## Overview 
The Recipe Dashboard is a web-based application designed to provide users with easy
access to recipe information. 


**API: Recipe API** - TheMealDB
#### Features
1. Set Favorite Meals: 
2. Search Meals by Name:
general weather conditions. 
3. Filter meals by Ingredient: 
4. Filter Meals by Category:
5. Add their own meals to the database:
6. Make a shopping list:

Route Description:

Route: /create-account
  ● Request Type: POST
  ● Purpose: Creates a new user account with a username and password.
  ● Request Body:
    ○ username(String):User's chosen username.
    ○ password(String):User's chosen password.
  ● Response Format: JSON
    ○ Success Response Example:
      ■ Code: 201
      ■ Content: { 'status': 'user added', 'username': <User's chosen username> }
  ● Example Request:
             {
                  'username': 'newuser123',
                  'password': 'securepassword'
  }
  ● Example Response:
             {
                  'status': 'user added', 'username': 'newuser123'
  }

Route: /delete-account
  ● Request Type: DELETE
  ● Purpose: Delete an existing user account with a username.
  ● Request Body:
    ○ username(String): Deleting account's username.
  ● Response Format: JSON
    ○ Success Response Example:
      ■ Code: 200
      ■ Content: { 'status': 'user deleted', 'username': <Deleting account's username> }
  ● Example Request:
             {
                  'username': 'newuser123'
  }
  ● Example Response:
             {
                  'status': 'user deleted', 'username': 'newuser123'
  }  
  
Route: /login
  ● Request Type: POST
  ● Purpose: log in to an existing account with username and password.
  ● Request Body:
    ○ username(String): exisitng account's username.
    ○ password(String): existing account's password.
  ● Response Format: JSON
    ○ Success Response Example:
      ■ Code: 200
      ■ Content: { "message": "User <account's username> logged in successfully." }
  ● Example Request:
             {
                  'username': 'newuser123'
                  'password': 'securepassword'
  }
  ● Example Response:
             {
                  "message": "User newuser123 logged in successfully."
  }  
  
Route: /logout
  ● Request Type: POST
  ● Purpose: log out of a logged in account.
  ● Request Body:
    ○ username(String): logged in account's username.
  ● Response Format: JSON
    ○ Success Response Example:
      ■ Code: 200
      ■ Content: { "message": "User <logged in account's username> logged out successfully. }
  ● Example Request:
             {
                  'username': 'newuser123'
  }
  ● Example Response:
             {
                  "message": "User newuser123 logged out successfully."
  }  
