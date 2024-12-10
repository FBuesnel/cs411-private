from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, Response, request
from werkzeug.exceptions import BadRequest, Unauthorized
# from flask_cors import CORS

from config import ProductionConfig
from recipe.db import db
from recipe.models.themealdb_model import RecipeAPI
from recipe.models.recipe_model import Meal
from recipe.models.mongo_session_model import login_user, logout_user
from recipe.models.user_model import Users
from recipe.models.recipe_model import RecipeManager

recipe_api = RecipeAPI()

# Load environment variables from .env file
load_dotenv()

def create_app(config_class=ProductionConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)  # Initialize db with app
    with app.app_context():
        db.create_all()  # Recreate all tables

    # battle_model = BattleModel()

    ####################################################
    #
    # Healthchecks
    #
    ####################################################


    @app.route('/api/health', methods=['GET'])
    def healthcheck() -> Response:
        """
        Health check route to verify the service is running.

        Returns:
            JSON response indicating the health status of the service.
        """
        app.logger.info('Health check')
        return make_response(jsonify({'status': 'healthy'}), 200)

    ##########################################################
    #
    # User management
    #
    ##########################################################

    @app.route('/api/create-user', methods=['POST'])
    def create_user() -> Response:
        """
        Route to create a new user.

        Expected JSON Input:
            - username (str): The username for the new user.
            - password (str): The password for the new user.

        Returns:
            JSON response indicating the success of user creation.
        Raises:
            400 error if input validation fails.
            500 error if there is an issue adding the user to the database.
        """
        app.logger.info('Creating new user')
        try:
            # Get the JSON data from the request
            data = request.get_json()

            # Extract and validate required fields
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return make_response(jsonify({'error': 'Invalid input, both username and password are required'}), 400)

            # Call the User function to add the user to the database
            app.logger.info('Adding user: %s', username)
            Users.create_user(username, password)

            app.logger.info("User added: %s", username)
            return make_response(jsonify({'status': 'user added', 'username': username}), 201)
        except Exception as e:
            app.logger.error("Failed to add user: %s", str(e))
            return make_response(jsonify({'error': str(e)}), 500)

    @app.route('/api/delete-user', methods=['DELETE'])
    def delete_user() -> Response:
        """
        Route to delete a user.

        Expected JSON Input:
            - username (str): The username of the user to be deleted.

        Returns:
            JSON response indicating the success of user deletion.
        Raises:
            400 error if input validation fails.
            500 error if there is an issue deleting the user from the database.
        """
        app.logger.info('Deleting user')
        try:
            # Get the JSON data from the request
            data = request.get_json()

            # Extract and validate required fields
            username = data.get('username')

            if not username:
                return make_response(jsonify({'error': 'Invalid input, username is required'}), 400)

            # Call the User function to delete the user from the database
            app.logger.info('Deleting user: %s', username)
            Users.delete_user(username)

            app.logger.info("User deleted: %s", username)
            return make_response(jsonify({'status': 'user deleted', 'username': username}), 200)
        except Exception as e:
            app.logger.error("Failed to delete user: %s", str(e))
            return make_response(jsonify({'error': str(e)}), 500)

    @app.route('/api/login', methods=['POST'])
    def login():
        """
        Route to log in a user and load their recipe.

        Expected JSON Input:
            - username (str): The username of the user.
            - password (str): The user's password.

        Returns:
            JSON response indicating the success of the login.

        Raises:
            400 error if input validation fails.
            401 error if authentication fails (invalid username or password).
            500 error for any unexpected server-side issues.
        """
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            app.logger.error("Invalid request payload for login.")
            raise BadRequest("Invalid request payload. 'username' and 'password' are required.")

        username = data['username']
        password = data['password']

        try:
            # Validate user credentials
            if not Users.check_password(username, password):
                app.logger.warning("Login failed for username: %s", username)
                raise Unauthorized("Invalid username or password.")

            # Get user ID
            user_id = Users.get_id_by_username(username)

            # Load user's combatants into the battle model
            login_user(user_id, RecipeManager)

            app.logger.info("User %s logged in successfully.", username)
            return jsonify({"message": f"User {username} logged in successfully."}), 200

        except Unauthorized as e:
            return jsonify({"error": str(e)}), 401
        except Exception as e:
            app.logger.error("Error during login for username %s: %s", username, str(e))
            return jsonify({"error": "An unexpected error occurred."}), 500


    @app.route('/api/logout', methods=['POST'])
    def logout():
        """
        Route to log out a user and save their recipes to MongoDB.

        Expected JSON Input:
            - username (str): The username of the user.

        Returns:
            JSON response indicating the success of the logout.

        Raises:
            400 error if input validation fails or user is not found in MongoDB.
            500 error for any unexpected server-side issues.
        """
        data = request.get_json()
        if not data or 'username' not in data:
            app.logger.error("Invalid request payload for logout.")
            raise BadRequest("Invalid request payload. 'username' is required.")

        username = data['username']

        try:
            # Get user ID
            user_id = Users.get_id_by_username(username)

            # Save user's combatants and clear the battle model
            logout_user(user_id, RecipeManager)

            app.logger.info("User %s logged out successfully.", username)
            return jsonify({"message": f"User {username} logged out successfully."}), 200

        except ValueError as e:
            app.logger.warning("Logout failed for username %s: %s", username, str(e))
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            app.logger.error("Error during logout for username %s: %s", username, str(e))
            return jsonify({"error": "An unexpected error occurred."}), 500


    ##########################################################
    #
    # Meals
    #
    ##########################################################


    @app.route('/api/search-meals', methods=['GET'])
    def search_meals() -> Response:
        """
        Route to search for meals by their name.

        Query Parameters:
            - name (str): The name of the meal to search for.

        Returns:
            JSON response with the list of meals matching the search query.
        Raises:
            400 error if the meal name is not provided.
            500 error if there is an issue fetching meals.
        """
        try:
            meal_name = request.args.get('name')
            if not meal_name:
                app.logger.error("Meal name is required.")
                return make_response(jsonify({"error": "Meal name is required"}), 400)

            app.logger.info(f"Searching meals by name: {meal_name}")
            meals = recipe_api.search_meals_by_name(meal_name)
            return make_response(jsonify({'meals': meals}), 200)
        except Exception as e:
            app.logger.error(f"Error searching meals: {e}")
            return make_response(jsonify({"error": str(e)}), 500)

    @app.route('/api/meal-details/<int:meal_id>', methods=['GET'])
    def get_meal_details(meal_id: int) -> Response:
        """
        Route to fetch details of a meal by its ID.

        Path Parameters:
            - meal_id (int): The ID of the meal.

        Returns:
            JSON response with the meal details.
        Raises:
            404 error if the meal is not found.
            500 error if there is an issue fetching meal details.
        """
        try:
            app.logger.info(f"Fetching details for meal ID: {meal_id}")
            details = recipe_api.get_meal_details(meal_id)
            if not details:
                app.logger.warning(f"Meal ID {meal_id} not found.")
                return make_response(jsonify({"error": "Meal not found"}), 404)
            return make_response(jsonify({'meal': details}), 200)
        except Exception as e:
            app.logger.error(f"Error fetching meal details: {e}")
            return make_response(jsonify({"error": str(e)}), 500)

    @app.route('/api/random-meal', methods=['GET'])
    def random_meal() -> Response:
        """
        Route to fetch a random meal.

        Returns:
            JSON response with the details of a random meal.
        Raises:
            500 error if there is an issue fetching a random meal.
        """
        try:
            app.logger.info("Fetching a random meal.")
            meal = recipe_api.get_random_meal()
            if not meal:
                app.logger.error("No random meal fetched.")
                return make_response(jsonify({"error": "Could not fetch a random meal"}), 500)
            return make_response(jsonify({'meal': meal}), 200)
        except Exception as e:
            app.logger.error(f"Error fetching random meal: {e}")
            return make_response(jsonify({"error": str(e)}), 500)

    @app.route('/api/meals-by-letter/<string:letter>', methods=['GET'])
    def meals_by_letter(letter: str) -> Response:
        """
        Route to list meals by their first letter.

        Path Parameters:
            - letter (str): The first letter of the meal name.

        Returns:
            JSON response with the list of meals starting with the given letter.
        Raises:
            400 error if the input is not a single letter.
            500 error if there is an issue fetching meals.
        """
        try:
            if len(letter) != 1:
                app.logger.error("Invalid input. A single letter is required.")
                return make_response(jsonify({"error": "Only a single letter is allowed"}), 400)

            app.logger.info(f"Listing meals by the first letter: {letter}")
            meals = recipe_api.list_meals_by_first_letter(letter)
            return make_response(jsonify({'meals': meals}), 200)
        except Exception as e:
            app.logger.error(f"Error listing meals by first letter: {e}")
            return make_response(jsonify({"error": str(e)}), 500)

    @app.route('/api/meals-by-ingredient', methods=['GET'])
    def meals_by_ingredient() -> Response:
        """
        Route to filter meals by a specific ingredient.

        Query Parameters:
            - ingredient (str): The ingredient to filter meals by.

        Returns:
            JSON response with the list of meals containing the specified ingredient.
        Raises:
            400 error if the ingredient is not provided.
            500 error if there is an issue fetching meals.
        """
        try:
            ingredient = request.args.get('ingredient')
            if not ingredient:
                app.logger.error("Ingredient is required.")
                return make_response(jsonify({"error": "Ingredient is required"}), 400)

            app.logger.info(f"Filtering meals by ingredient: {ingredient}")
            meals = recipe_api.filter_meals_by_ingredient(ingredient)
            return make_response(jsonify({'meals': meals}), 200)
        except Exception as e:
            app.logger.error(f"Error filtering meals by ingredient: {e}")
            return make_response(jsonify({"error": str(e)}), 500)

    return app


if __name__ == '__main__':

    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)