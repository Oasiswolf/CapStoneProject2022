from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://wccaegsmvhvykt:c1d3281bddeede409f966c67423aa71dfa2169fab132a64d932740424beea023@ec2-44-214-132-149.compute-1.amazonaws.com:5432/dfmkn6n237qikb"

# /////// API Hosted lilnk name \\\\\\\\\\\\\\\\
# https://jukebox-wood-crafts.herokuapp.com/(add wanted endpoint)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    category = db.Column(db.String)
    item_img = db.Column(db.String, unique=True)

    def __init__(self, title, category, item_img):
        self.title = title
        self.category = category
        self.item_img = item_img

class ItemSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'category', 'item_img')

item_schema = ItemSchema()
multi_item_schema = ItemSchema(many=True)

# /////////////////// How to Add items to the Database \\\\\\\\\\\\\\\
@app.route('/item/add', methods=["POST"])
def add_item():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be sent as JSON')

    post_data = request.get_json()
    title = post_data.get('title')
    category = post_data.get('category')
    item_img = post_data.get('item_img')

    if title == None:
        return jsonify("Error: You must provide an 'Item Title' key")
    if item_img == None:
        return jsonify("Error: You must provide a 'Picture' key")

    new_record = Item(title, category, item_img)
    db.session.add(new_record)
    db.session.commit()

    return jsonify(item_schema.dump(new_record))

# /////////////////// How to Get all items from the Database \\\\\\\\\\\\\\\

@app.route('/item/get', methods=["GET"])
def get_all_items():
    all_records = db.session.query(Item).all()
    return jsonify(multi_item_schema.dump(all_records))

# /////////////////// How to Get items by ID from the Database \\\\\\\\\\\\\\\

@app.route('/item/get/<id>', methods=["GET"])
def get_item_id(id):
    one_item = db.session.query(Item).filter(Item.id == id).first()
    return jsonify(item_schema.dump(one_item))

# /////////////////// How to Update Items to the Database \\\\\\\\\\\\\\\
@app.route('/item/update/<id>', methods=["PUT"])
def update_item(id):
    if request.content_type != 'application/json':
        return jsonify("Error: Datamust be sent as JSON")

    put_data = request.get_json()
    title = put_data.get('title')
    category = put_data.get('category')
    item_img = put_data.get('item_img')

    item_to_update = db.session.query(Item).filter(Item.id == id).first()

    if title != None:
        item_to_update.title = title
    if category != None:
        item_to_update.category = category
    if item_img != None:
        item_to_update.item_img = item_img

    db.session.commit()

    return jsonify(item_schema.dump(item_to_update))

# ///////////////////How to Add Multiple Items to he Database \\\\\\\\\\\\\\\\\\\

@app.route('/item/add/multi', methods=["POST"])
def add_multi_items():
    if request.content_type != "application/json":
        return jsonify("ERROR: Data must be sent as JSON")
    
    post_data = request.get_json()

    new_records = []

    for item in post_data:
        title = item.get('title')
        category = item.get('category')
        item_img = item.get('item_img')

        existing_item_check = db.session.query(Item).filter(item.title == title).first()
        if existing_item_check is None:
            new_record = item(title, category, item_img)
            db.session.add(new_record)
            db.session.commit()
            new_records.append(new_record)

        return jsonify(multi_item_schema.dump(new_records))



    # /////////////////// How to Delete Items from the Database \\\\\\\\\\\\\\\
@app.route('/item/delete/<id>', methods=["DELETE"])
def item_to_delete(id):
    delete_item = db.session.query(Item).filter(Item.id == id).first()
    db.session.delete(delete_item)
    db.session.commit()
    return jsonify("Item was Deleted Successfully")


































if __name__ == "__main__":
    app.run(debug = True)