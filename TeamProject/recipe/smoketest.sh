#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5000/api"

# Flag to control whether to echo JSON output
ECHO_JSON=false

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done


###############################################
#
# Health checks
#
###############################################

# Function to check the health of the service
check_health() {
  echo "Checking health status..."
  curl -s -X GET "$BASE_URL/health" | grep -q '"status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    exit 1
  fi
}

##############################################
#
# User management
#
##############################################

# Function to create a user
create_user() {
  echo "Creating a new user..."
  curl -s -X POST "$BASE_URL/create-user" -H "Content-Type: application/json" \
    -d '{"username":"testuser", "password":"password123"}' | grep -q '"status": "user added"'
  if [ $? -eq 0 ]; then
    echo "User created successfully."
  else
    echo "Failed to create user."
    exit 1
  fi
}

# Function to log in a user
login_user() {
  echo "Logging in user..."
  response=$(curl -s -X POST "$BASE_URL/login" -H "Content-Type: application/json" \
    -d '{"username":"testuser", "password":"password123"}')
  if echo "$response" | grep -q '"message": "User testuser logged in successfully."'; then
    echo "User logged in successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Login Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to log in user."
    if [ "$ECHO_JSON" = true ]; then
      echo "Error Response JSON:"
      echo "$response" | jq .
    fi
    exit 1
  fi
}

# Function to log out a user
logout_user() {
  echo "Logging out user..."
  response=$(curl -s -X POST "$BASE_URL/logout" -H "Content-Type: application/json" \
    -d '{"username":"testuser"}')
  if echo "$response" | grep -q '"message": "User testuser logged out successfully."'; then
    echo "User logged out successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Logout Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to log out user."
    if [ "$ECHO_JSON" = true ]; then
      echo "Error Response JSON:"
      echo "$response" | jq .
    fi
    exit 1
  fi
}

##############################################
#
# Meals
#
##############################################

# Function to search for a meal
search_meals() {
  meal_name=$1

  echo "Searching meals by name Spicy Arrabiata Penne..."
  response=$(curl -s -X GET "$BASE_URL/search-meals?name=Spicy%20Arrabiata%20Penne")

  if echo "$response" | grep -q '"meals"'; then
    echo "Meals retrieved successfully for query: Spicy Arrabiata Penne."
    if [ "$ECHO_JSON" = true ]; then
      echo "Meals JSON:"
      echo "$response" | jq .
    fi
  elif echo "$response" | grep -q '"error": "Meal name is required"'; then
    echo "Error: Meal name is required. Please provide a valid meal name."
    exit 1
  else
    echo "Failed to search meals for query: $meal_name."
    echo "Response: $response"
    exit 1
  fi
}


# Function to get meal details
get_meal_details() {
  meal_id=$1

  echo "Fetching details for meal ID 52771..."
  response=$(curl -s -X GET "$BASE_URL/meal-details/52771")

  if echo "$response" | grep -q '"meal"'; then
    echo "Meal details retrieved successfully for ID: 52771."
    if [ "$ECHO_JSON" = true ]; then
      echo "Meal Details JSON:"
      echo "$response" | jq .
    fi
  elif echo "$response" | grep -q '"error": "Meal not found"'; then
    echo "Error: Meal not found for ID: $meal_id."
    exit 1
  else
    echo "Failed to fetch details for meal ID: $meal_id."
    echo "Response: $response"
    exit 1
  fi
}

# Function to fetch random meal
random_meal() {
  echo "Fetching a random meal..."
  response=$(curl -s -X GET "$BASE_URL/random-meal")

  if echo "$response" | grep -q '"meal"'; then
    echo "Random meal fetched successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Random Meal JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to fetch a random meal."
    echo "Response: $response"
    exit 1
  fi
}

# Function to list meals by first letter
meals_by_letter() {
  letter=$1

  echo "Fetching meals starting with the letter S..."
  response=$(curl -s -X GET "$BASE_URL/meals-by-letter/S")

  if echo "$response" | grep -q '"meals"'; then
    echo "Meals starting with the letter S retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Meals JSON:"
      echo "$response" | jq .
    fi
  elif echo "$response" | grep -q '"error": "Only a single letter is allowed"'; then
    echo "Error: Only a single letter is allowed. Invalid input: $letter."
    exit 1
  else
    echo "Failed to fetch meals starting with the letter: $letter."
    echo "Response: $response"
    exit 1
  fi
}


# Function to filter meals by ingredients
meals_by_ingredient() {
  ingredient=$1

  echo "Fetching meals containing the ingredient garlic..."
  response=$(curl -s -X GET "$BASE_URL/meals-by-ingredient?ingredient=garlic")

  if echo "$response" | grep -q '"meals"'; then
    echo "Meals containing the ingredient garlic retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Meals JSON:"
      echo "$response" | jq .
    fi
  elif echo "$response" | grep -q '"error": "Ingredient is required"'; then
    echo "Error: Ingredient is required. Please provide a valid ingredient."
    exit 1
  else
    echo "Failed to fetch meals containing the ingredient: $ingredient."
    echo "Response: $response"
    exit 1
  fi
}

# Function to initialize the database
init_db() {
  echo "Initializing the database..."
  response=$(curl -s -X POST "$BASE_URL/init-db")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Database initialized successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Initialization Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to initialize the database."
    exit 1
  fi
}



# Run all the steps in order
check_health
init_db
search_meals
get_meal_details
random_meal
meals_by_letter
meals_by_ingredient

echo "All tests passed successfully!"