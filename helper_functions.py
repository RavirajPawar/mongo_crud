def get_counter(mongo):
    "returns counter which is used as ID in appliction"
    output = mongo.db.templates.find_one_and_update(
        {"template_id": "Unique_Key_123"}, {"$inc": {"counter": 1}}
    )
    return output["counter"]


def add_template(mongo, data, current_user):
    """
    This functtion will add new document in db with addition of owner and id key
    inputs
    mongo:- mongo db connection object
    data:- user passed data
    current_user:- onwer of document
    returns
    message:- status message of operation
    """
    data["owner"] = current_user
    data["ID"] = get_counter(mongo)
    try:
        mongo.db.templates.insert_one(data)
        return {"message": "Template added successfully."}
    except:
        return {"message": "Try Again."}


def fetch_template(mongo, current_user, id=None):
    """
    This functtion will fetch all documents owned by user from db
    inputs
    mongo:- mongo db connection object
    current_user:- owner of documents
    id:- when want specific template
    return
    list of documents/templates added by owner
    """
    try:
        if id:
            owner_template = mongo.db.templates.find_one(
                {"owner": current_user, "ID": int(id)}, {"_id": False, "owner": False}
            )
            if owner_template == None:
                owner_template = {"message": "please enter valid ID"}

        else:
            owner_template = mongo.db.templates.find(
                {"owner": current_user}, {"_id": False, "owner": False}
            )
            owner_template = [template for template in owner_template]
        return owner_template

    except ValueError:
        return {"message": "Please enter numbers for id"}

    except:
        return {"message": "Try Again."}


def remove_template(mongo, current_user, id):
    """
    removes template from database using ID and email
    inputs
    mongo:- mongo connection object
    current_user- owner of documents
    id:- ID of document
    returns
    dict of status message
    """
    try:
        removed_document = mongo.db.templates.delete_one(
            {"owner": current_user, "ID": int(id)}
        )
        if removed_document.deleted_count > 0:
            return {"mesage": "Deleted record"}
        else:
            return {"mesage": "Please Enter ID belongs to you"}

    except ValueError:
        return {"message": "Please enter number for id"}

    except Exception as e:
        return {"mesage": "Try Again", "exp": e}


def update_template(mongo, current_user, data, id):
    try:
        data["owner"] = current_user
        data["ID"] = int(id)

        updated_record = mongo.db.templates.update_one(
            {"owner": current_user, "ID": int(id)}, {"$set": data}
        )

        return {"mesage": "Updated record"}

    except ValueError as e:
        return {"message": "Please enter number for id", "exp": str(e)}

    except Exception as e:
        return {"mesage": "Try Again", "exp": str(e)}
