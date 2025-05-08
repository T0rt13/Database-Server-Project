from influx_cmds import DBInflux
from file_uploading import BlobOperations
from db_ops import MariaDB

# create instances
influx_client = DBInflux()
blob_client = BlobOperations()
SQL_client = MariaDB()
connection_to_SQL = SQL_client.get_connection_with_db()

# operation 1, Upload a post
def createpost(postID, postuser, posttitle, postfilepath, postfilename):
    SQL_client.insert_post(connection_to_SQL, postID, postuser, posttitle, postfilename)
    influx_client.create_post(postuser, postID)
    blob_client.query1_createfile(postfilepath, postfilename)

# operation 2, List posts by most recent
def getposts(time_range):
    recent_posts = influx_client.get_recent_posts(time_range)
    # print(recent_posts)
    for post_id in recent_posts:
        print(f"Post: {post_id}")
        post = SQL_client.get_post(connection_to_SQL, post_id)
        if post:
            file = blob_client.query3_getbloburl(post["file_name"])
        else:
            file = ""
            post = "Deleted"
        print("Relational:", post)
        print("len() of object:", len(file))

# operation 3, Get details of the post
def detailpost(post_id):
    post = SQL_client.get_post(connection_to_SQL, post_id)
    if post:
        file = blob_client.query3_getbloburl(post["file_name"])
        time_info = influx_client.get_post_most_recent_timestamp(post["post_id"], "1d")
    else:
        file = ""
        time_info = "N/A"
        post = "Deleted"
    print("Relational:", post, "\nTime:", time_info, "\nlen() of object:", len(file))

# operation 4, Delete a post
def deletepost(post_id, user_id):
    post = SQL_client.get_post(connection_to_SQL, post_id)
    influx_client.delete_post(user_id,post_id)
    blob_client.query4_deleteblob(post["file_name"])
    SQL_client.soft_delete_post(connection_to_SQL, post_id)
    print(f"Post {post_id} Deleted")

# operation 5, Edit a post
def editpost(post_id, posttitle, postfilepath, postfilename):
    post = SQL_client.get_post(connection_to_SQL, post_id)
    if postfilename != None and postfilepath != None:
        # edit file if there is one, otherwise add a file
        if post["file_name"]:
            blob_client.query5_editblob(post["file_name"], postfilepath, postfilename)
            SQL_client.update_post(connection_to_SQL, post_id, posttitle, postfilename)
        else:
            blob_client.query1_createfile(postfilepath, postfilename)
            SQL_client.update_post(connection_to_SQL, post_id, posttitle, postfilename)

    print("Post", post_id, "has been updated.")
    detailpost(post_id)

# operation 6, Upvote a post
def upvote_post(post_id, user_id):
    SQL_client.upvote_post(connection_to_SQL, post_id, user_id)
    influx_client.upvote_post(user_id, post_id)
    print("Post:", post_id, "has been upvoted.")


# test 6 operations
if __name__ == "__main__":
    print("Creating 2 separate posts (operation 1).")
    print("In the relational database, they will look like:")
    print("   post_id=post1, user_id=Pete, title=Pizza, file_name=pizza.jpg, status=active")
    print("   post_id=post2, user_id=Tim, title=Taco, file_name=pizza.jpg, status=active")
    print("Images will be added to the object database, and timestamps added to the time-series database")
    createpost("post1", "Pete", "Pizza", "./", "pizza.jpg")
    createpost("post2", "Tim", "Taco", "./", "taco.jpg")
    print()

    print("Getting most recent posts in last day (operation 2).")
    getposts("1d")
    print("len() was used to approximate file size. Easier than displaying image.")
    print()

    print("Getting details of post2 (operation 3).")
    detailpost("post2")
    print()

    print("Deleting post2 (operation 4).")
    deletepost("post2", "Tim")
    print()

    print("Editing post1 (operation 5).")
    editpost("post1", "Now, a taco!", "./", "taco.jpg")
    print()

    print("Upvoting post1 (operation 6).")
    upvote_post("post1", "Katie")
    print()

    print("Final post information from the last day:")
    getposts("1d")
