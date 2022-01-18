from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://legghaaryteyxf:37613d5242a83640752f3eae39573cf3575305babd1bb22d87719780776996d7@ec2-54-208-139-247.compute-1.amazonaws.com:5432/d3cddarv8stsml"

# /////// API Hosted lilnk name \\\\\\\\\\\\\\\\
# https://jukebox-wood-crafts.herokuapp.com/(add wanted endpoint)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Picture(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    item_title = db.Column(db.String, nullable=False)
    category = db.Column(db.String)
    item_img = db.Column(db.String, unique=True)

    def __init__(self, item_title, category, item_img):
        self.item_title = item_title
        self.category = category
        self.item_img = item_img

class PictureSchema(ma.Schema):
    class Meta:
        fields = ('id', 'item_title', 'category', 'item_img')

picture_schema = PictureSchema()
multi_picture_schema = PictureSchema(many=True)

# /////////////////// How to Add items to the Database \\\\\\\\\\\\\\\
@app.route('/item/add', methods=["POST"])
def add_item():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be sent as JSON')

    post_data = request.get_json()
    item_title = post_data.get('item_title')
    category = post_data.get('category')
    item_img = post_data.get('item_img')

    if item_title == None:
        return jsonify("Error: You must provide an 'Item Title' key")
    if item_img == None:
        return jsonify("Error: You must provide a 'Picture' key")

    new_record = Picture(item_title, category, item_img)
    db.session.add(new_record)
    db.session.commit()

    return jsonify(picture_schema.dump(new_record))

# /////////////////// How to Get all items from the Database \\\\\\\\\\\\\\\

@app.route('/item/get', methods=["GET"])
def get_all_items():
    all_records = db.session.query(Picture).all()
    return jsonify(multi_picture_schema.dump(all_records))

# /////////////////// How to Get items by ID from the Database \\\\\\\\\\\\\\\
@app.route('/item/get/<id>', methods=["GET"])
def get_item_id(id):
    one_item = db.session.query(Picture).filter(Picture.id == id).first()
    return jsonify(picture_schema.dump(one_item))


# /////////////////// How to Update Items to the Database \\\\\\\\\\\\\\\
@app.route('/item/update/<id>', methods=["PUT"])
def update_item(id):
    if request.content_type != 'application/json':
        return jsonify("Error: Datamust be sent as JSON")

    put_data = request.get_json()
    item_title = put_data.get('item_title')
    category = put_data.get('category')
    item_img = put_data.get('item_img')

    item_to_update = db.session.query(Picture).filter(Picture.id == id).first()

    if item_title != None:
        item_to_update.item_title = item_title
    if category != None:
        item_to_update.category = category
    if item_img != None:
        item_to_update.item_img = item_img

    db.session.commit()

    return jsonify(picture_schema.dump(item_to_update))

# ///////////////////How to Add Multiple Items to he Database \\\\\\\\\\\\\\\\\\\
app.route('/item/add/multi', methods=["POST"])
def add_multi_items():
    if request.content_type != "application/json":
        return jsonify("ERROR: Data must be sent as JSON")
    
    post_data = request.get_json()

    new_records = []

    for picture in post_data:
        item_title = picture.get('item_title')
        category = picture.get('category')
        item_img = picture.get('item_img')

        existing_item_check = db.session.query(Picture).filter(Picture.item_title == item_title).first()
        if existing_item_check is None:
            new_record = Picture(item_title, category, item_img)
            db.session.add(new_record)
            db.session.commit()
            new_records.append(new_record)

        return jsonify(multi_picture_schema.dump(new_records))



    # /////////////////// How to Delete Items from the Database \\\\\\\\\\\\\\\
@app.route('/item/delete/<id>', methods=["DELETE"])
def item_to_delete(id):
    delete_item = db.session.query(Picture).filter(Picture.id == id).first()
    db.session.delete(delete_item)
    db.session.commit()
    return jsonify("Item was Deleted Successfully")


































if __name__ == "__main__":
    app.run(debug = True)