from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

uri = "mongodb+srv://Apiwit:192922@cluster0.k7xei6x.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["Store"]
collection = db["products"]

@app.route("/")
def greet():
    return "<p>Welcome to Shop Notebook </p>"

@app.route("/products", methods=["GET"])
def get_all_products():
    products = list(collection.find())
    return jsonify(products)

@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = collection.find_one({"_id": product_id})
    if product:
        return jsonify(product)
    else:
        return jsonify({"error": "product not found"}), 404


@app.route("/products", methods=["POST"])
def create_products():
    data = request.get_json()
   
    if collection.find_one({"_id":data["_id"]}):
        return jsonify({"error": "Notebook with the same ID already exists"}), 409
    else:
        collection.insert_one(data)
        return jsonify('Sucess'),200



    
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_products(product_id):
    data = request.get_json()

    existing_product = collection.find_one({"_id": product_id})

    if existing_product:
        collection.update_one({"_id": product_id}, {"$set": data})
        return jsonify(data)
    else:
        return jsonify({"error": "product not found"}), 404
    
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_products(product_id):
    existing_product = collection.find_one({"_id": product_id})
 
    if existing_product:
        collection.delete_one({"_id": product_id})
        return jsonify({"message": "product deleted successfully"}), 200
    else:
        return jsonify({"error": "product not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
