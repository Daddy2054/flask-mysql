#comment: if lib not present do pip/pip3 install flask :)
from flask import Flask, request, jsonify
import pymysql
from flask_cors import CORS

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'db-78n9n',
    'database': 'test'
}
db_comm = pymysql.connect(**db_config) 
cursor = db_comm.cursor()
app = Flask(__name__)
CORS(app)

# Sample data - You can replace this with your own data storage or database


# Route to get all items
@app.route('/items', methods=['GET'])
def get_items():
   try:
      cursor.execute("SELECT * FROM items2")
      items = [{'id':id, 'name':name,} for id, name in cursor.fetchall()]
      return jsonify(items)
   except Exception as e:
      return jsonify({'error': str(e)}), 500

#route to insert items
@app.route('/items', methods=['POST'])
def add_item():
   try:
      data = request.get_json()
      name = data['name']
      cursor.execute("INSERT INTO items2 (name) VALUES (%s)", (name,))
      db_comm.commit()
      return jsonify({'message': 'Item added successfully'})
   except Exception as e:
      return jsonify({'error': str(e)}), 500

# route to update items
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
   try:
      data = request.get_json()
      name = data['name']
      cursor.execute("UPDATE items2 SET name=%s WHERE id=%s", (name, item_id))
      db_comm.commit()
      return jsonify({'message': 'Item updated successfully'})
   except Exception as e:
      return jsonify({'error': str(e)}), 500
   
#route do delete items
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
   try:
      cursor.execute("DELETE FROM items2 WHERE id=%s", (item_id,))
      db_comm.commit()
      return jsonify({'message': 'Item deleted successfully'})
   except Exception as e:
      return jsonify({'error': str(e)}), 500
   
if __name__ == '__main__':
   app.run(debug=True)
