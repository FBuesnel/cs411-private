# Recipe Application Dashboard

## Overview
The Recipe Dashboard is a web-based application designed to provide users with easy access to recipe information. This application allows users to set favorite meals and quickly search for, filter, and explore recipes based on ingredients, categories, or meal names. The Recipe Dashboard aims to deliver a personalized recipe discovery experience, making it easier for users to find the most relevant recipes based on their preferences and dietary needs while allowing for the creation of shopping lists to easily buy all the ingredients.

**API: Recipe API** - TheMealDB


## Routes Documentation

### User Account Management

#### Create Account
**Route:** `/create-account`  
**Request Type:** `POST`

**Purpose:** Creates a new user account with a username and password.

**Request Body:**
```json
{
    "username": "newuser123",
    "password": "securepassword"
}
```

**Response Format:** JSON
- **Success Response Example:**
    ```json
    {
        "status": "user added",
        "username": "newuser123"
    }
    ```

---

#### Delete Account
**Route:** `/delete-account`  
**Request Type:** `DELETE`

**Purpose:** Deletes an existing user account by username.

**Request Body:**
```json
{
    "username": "newuser123"
}
```

**Response Format:** JSON
- **Success Response Example:**
    ```json
    {
        "status": "user deleted",
        "username": "newuser123"
    }
    ```

---

#### Login
**Route:** `/login`  
**Request Type:** `POST`

**Purpose:** Logs in to an existing account with username and password.

**Request Body:**
```json
{
    "username": "newuser123",
    "password": "securepassword"
}
```

**Response Format:** JSON
- **Success Response Example:**
    ```json
    {
        "message": "User newuser123 logged in successfully."
    }
    ```

---

#### Logout
**Route:** `/logout`  
**Request Type:** `POST`

**Purpose:** Logs out of a logged-in account.

**Request Body:**
```json
{
    "username": "newuser123"
}
```

**Response Format:** JSON
- **Success Response Example:**
    ```json
    {
        "message": "User newuser123 logged out successfully."
    }
    ```

---

### Recipe Management

#### Search Meals by Name
**Route:** `/api/search-meals`  
**Request Type:** `GET`

**Purpose:** Searches for meals by their name.

**Query Parameters:**
- `name` (String): The name of the meal to search for.

**Response Format:** JSON
- **Success Response Example:**
    ```json
    {
        "meals": [
            { "id": 123, "name": "Pasta", "category": "Italian" }
        ]
    }
    ```

---

#### Get Meal Details
**Route:** `/api/meal-details/<int:meal_id>`  
**Request Type:** `GET`

**Purpose:** Fetches details of a meal by its ID.

**Path Parameters:**
- `meal_id` (Integer): The ID of the meal.

**Response Format:** JSON
- **Success Response Example:**
    ```json
    {
        "meal": {
            "id": 123,
            "name": "Pasta",
            "ingredients": ["Flour", "Eggs", "Tomato Sauce"]
        }
    }
    ```

---

#### Fetch Random Meal
**Route:** `/api/random-meal`  
**Request Type:** `GET`

**Purpose:** Fetches a random meal.

**Response Format:** JSON
- **Success Response Example:**
    ```json
    {
        "meal": {
            "id": 456,
            "name": "Pizza",
            "ingredients": ["Dough", "Cheese", "Tomato Sauce"]
        }
    }
    ```

---

#### List Meals by First Letter
**Route:** `/api/meals-by-letter/<string:letter>`  
**Request Type:** `GET`

**Purpose:** Lists meals by their first letter.

**Path Parameters:**
- `letter` (String): The first letter of the meal name.

**Response Format:** JSON
- **Success Response Example:**
    ```json
    {
        "meals": [
            { "id": 789, "name": "Apple Pie" }
        ]
    }
    ```

---

#### Filter Meals by Ingredient
**Route:** `/api/meals-by-ingredient`  
**Request Type:** `GET`

**Purpose:** Filters meals by a specific ingredient.

**Query Parameters:**
- `ingredient` (String): The ingredient to filter meals by.

**Response Format:** JSON
- **Success Response Example:**
    ```json
    {
        "meals": [
            { "id": 321, "name": "Egg Salad" }
        ]
    }
    ```

