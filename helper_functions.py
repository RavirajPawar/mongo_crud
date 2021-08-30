def get_counter(mongo):
    "returns counter which is used as ID in for each document."

    output = mongo.db.templates.find_one_and_update(
        {"template_id": "Unique_Key_123"}, {"$inc": {"counter": 1}}
    )
    return output["counter"]


def add_template(mongo, data, current_user):
    """
    This functtion will add new template with addition of owner and id key in document.
        Returns dict with message key.

    Arguments:

    mongo -- Flask mongo db connection object

    data -- user passed data to insert in database

    current_user -- owner of document/logged in user
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
    This functtion will fetch all documents owned by user if not specific ID is not passed
    else give specific template.
        Returns dict with message key.

    Arguments:

    mongo -- Flask mongo db connection object

    current_user -- owner of document/logged in user

    id:- when want specific template

    """
    try:
        if id:
            owner_template = mongo.db.templates.find_one(
                {"owner": current_user, "ID": int(id)},
                {"_id": False, "owner": False}
            )
            if owner_template == None:
                owner_template = {
                    "message": "please enter valid ID which belongs to you."}

        else:
            owner_template = mongo.db.templates.find(
                {"owner": current_user}, {"_id": False, "owner": False}
            )
            owner_template = [template for template in owner_template]
        return owner_template

    except ValueError:
        return {"message": "Please enter Integer for id"}

    except:
        return {"message": "Try Again."}


def remove_template(mongo, current_user, id):
    """
    This function will remove template which belongs to perticular user.
        Returns dict with message key.

    Arguments:

    mongo -- Flask mongo db connection object

    current_user -- owner of document/logged in user

    id --- specific template ID
    """
    try:
        removed_document = mongo.db.templates.delete_one(
            {"owner": current_user, "ID": int(id)}
        )
        if removed_document.deleted_count > 0:
            return {"mesage": "Template Deleted"}
        else:
            return {"mesage": "Please Enter ID which belongs to you"}

    except ValueError:
        return {"message": "Please enter Integer for id"}

    except Exception:
        return {"mesage": "Try Again"}


def update_template(mongo, current_user, data, id):
    try:
        data["owner"] = current_user
        data["ID"] = int(id)

        updated_record = mongo.db.templates.update_one(
            {"owner": current_user, "ID": int(id)}, {"$set": data}
        )
        if updated_record.modified_count > 0:
            return {"mesage": "Updated record"}
        else:
            return {"mesage": "Please Enter ID which belongs to you"}

    except ValueError:
        return {"message": "Please enter Integer for id"}

    except Exception:
        return {"mesage": "Try Again"}
