from flask import Flask, render_template, request, redirect, url_for
from web3 import Web3, HTTPProvider
import json

blockchain='http://127.0.0.1:7545'

# Dictionary to store object IDs and their details
object_registry = {}

def connect():
    web3=Web3(HTTPProvider(blockchain))
    web3.eth.defaultAccount=web3.eth.accounts[0]

    artifact="../build/contracts/SharingApp.json"
    with open(artifact) as f:
        artifact_json=json.load(f)
        contract_abi=artifact_json['abi']
        contract_address=artifact_json['networks']['5777']['address']
    contract=web3.eth.contract(
        abi=contract_abi,
        address=contract_address
    )
    return contract,web3

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register_object", methods=["GET", "POST"])
def register_object():
    if request.method == "POST":
        # Get form data
        object_name = request.form["object_name"]
        object_name=str(object_name)
        object_description = request.form["object_description"]
        object_description=str(object_description)
        object_price = request.form["object_price"]
        object_price=int(object_price)
        contract,web3=connect()

        # Check if object ID already exists
        object_id = len(object_registry) + 1
        if object_id in object_registry:
            return "Object ID already exists. Please try again."

        # Register object on blockchain
        tx_hash = contract.functions.register_object(object_name, object_description, object_price).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)

        # Add object to registry
        object_registry[object_id] = {
            "name": object_name,
            "description": object_description,
            "price": object_price
        }

        return "Registration successful!"

    return render_template("register.html")

@app.route("/rent_object", methods=["GET", "POST"])
def rent_object():
    if request.method == "POST":
        # Get form data
        object_id = request.form["object_id"]
        object_id=int(object_id)
        contract,web3=connect()

        # Check if object ID exists and is valid for rent
        if object_id not in object_registry:
            return "Invalid object ID. Please try again."

        # Rent object on blockchain
        tx_hash = contract.functions.rent_object(object_id).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)

        return "You have rented the object"

    return render_template("rent.html")

@app.route('/return_object', methods=['GET','POST'])
def return_object():
    if request.method == "POST":
        # Get form data
        object_id = request.form["object_id"]
        object_id=int(object_id)
        contract,web3=connect()

        # Check if object ID exists and is valid for return
        if object_id not in object_registry:
            return "Invalid object ID. Please try again."

        # Return object on blockchain
        tx_hash = contract.functions.return_object(object_id).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)

        return "Returned successfully"

    return render_template("return.html")

if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )