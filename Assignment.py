from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
import mysql.connector
from mysql.connector import Error

app = Flask(__name__) 
ma = Marshmallow(app)


#create a schema
class MemberSchema(ma.Schema):
    id = fields.Int(required=True) 
    name = fields.String(required=True)
    age = fields.String(required=True)

    class Meta: #options object for a schema
        fields = ("id", "name", "age") 

member_schema = MemberSchema() 
members_schema = MemberSchema(many=True) 


# -------------------------------------------


def get_db_connection():
    """ Connect to the My SQL database and return the connection object """
    # database connection parameters
    db_name = "FitnessCenter_db"
    user = "root"
    password = "Kaa4@sql"
    host = "localhost"

    try:
        # attempting to establish a connection
        conn = mysql.connector.connect(
            database=db_name,
            user=user,
            password=password,
            host=host)
        
        print("Connected to MySQL database successfully")
        return conn
    
    except Error as e:
        print(f"Error: {e}")
        return None
    
#----------------------------------

@app.route('/members', methods=['GET'])
def get_members():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM Members"

        cursor.execute(query)

        members = cursor.fetchall()

        return members_schema.jsonify(members) 
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500
    
    finally:
        if conn and conn.is_connected:
            cursor.close()
            conn.close()


@app.route('/members', methods=["POST"])
def add_member():
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        new_member = (member_data['id'], member_data['name'], member_data['age'])

        query = "INSERT INTO Members (id, name, age) VALUES (%s, %s, %s)"

        cursor.execute(query, new_member)
        conn.commit()

        return jsonify({"message": "New Member added successfully"}), 201
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected:
            cursor.close()
            conn.close()


@app.route('/members/<int:id>', methods=["PUT"]) 
def update_members(id):
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        updated_member = (member_data["id"], member_data["name"], member_data["age"], id)

        query = "UPDATE Members SET id = %s, name = %s, age = %s WHERE id = %s"

        cursor.execute(query, updated_member)
        conn.commit()

        return jsonify({"message": "Updated the member successfully"}), 201
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected:
            cursor.close()
            conn.close()


@app.route('/members/<int:id>', methods=["DELETE"]) 
def delete_member(id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        member_to_remove = (id, )

        cursor.execute("SELECT * FROM Members WHERE id = %s", member_to_remove)
        customer = cursor.fetchone()
        if not customer:
            return jsonify({"error": "Member not found"}), 404
        
        query = "DELETE FROM Members WHERE id = %s"
        cursor.execute(query, member_to_remove)
        conn.commit()
        return jsonify({"message": "Member removed successfully"}), 201
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected:
            cursor.close()
            conn.close()


# ------------------------------------
#WorkoutSessions


class SessionSchema(ma.Schema):
    session_id = fields.Int(required=True) 
    member_id = fields.Int(required=True)
    session_date = fields.String(required=True)
    session_time = fields.String(required=True)
    activity = fields.String(required=True)

    class Meta: 
        fields = ("session_id", "member_id", "session_date", "session_time", "activity") 

session_schema = SessionSchema() 
sessions_schema = SessionSchema(many=True) 


@app.route('/workoutsessions', methods=["GET"])
def view_sessions():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM WorkoutSessions"

        cursor.execute(query)

        sessions = cursor.fetchall()

        return sessions_schema.jsonify(sessions) 
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500
    
    finally:
        if conn and conn.is_connected:
            cursor.close()
            conn.close()


@app.route('/workoutsessions', methods=["POST"])
def schedule_session():
    try:
        session_data = session_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        new_session = (session_data['session_id'], session_data['member_id'], session_data['session_date'], session_data["session_time"], session_data["activity"], id)

        query = "INSERT INTO WorkoutSessions (session_id, member_id, session_date, session_time, activity) VALUES (%s, %s, %s, %s, %s)"

        cursor.execute(query, new_session)
        conn.commit()

        return jsonify({"message": "New workout session added successfully"}), 201
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected:
            cursor.close()
            conn.close()



@app.route('/workoutsessions/<int:id>', methods=["PUT"]) 
def update_session(id):
    try:
        session_data = session_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        updated_session = (session_data['session_id'], session_data['member_id'], session_data['session_date'], session_data["session_time"], session_data["activity"], id)

        query = "UPDATE WorkoutSessions SET session_id = %s, member_id = %s, session_date = %s, session_time = %s, activity = %s, WHERE id = %s"

        cursor.execute(query, update_session)
        conn.commit()

        return jsonify({"message": "Updated the workout session successfully"}), 201
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected:
            cursor.close()
            conn.close()


@app.route('/workoutsessions/<int:id>', methods=["GET"])
def view_member_sessions(id): #retrieving all sessions for specific member
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)

        member_id = (id, )
        query = "SELECT * FROM WorkoutSessions WHERE member_id = %s"

        cursor.execute(query, member_id)

        member_sessions = cursor.fetchone()

        return session_schema.jsonify(member_sessions) 
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500
    
    finally:
        if conn and conn.is_connected:
            cursor.close()
            conn.close()


if __name__ == '__main__':
    app.run(debug=True)