from influx_cmds import DBInflux
from file_uploading import BlobOperations
# Example for influx
influx_client = DBInflux()
blob_client = BlobOperations()
user1 = 1
user2 = 2
post1 = 1
post2 = 2
influx_client.create_post(user1, post1)
influx_client.create_post(user2, post2)
influx_client.upvote_post(user1, post1)
influx_client.upvote_post(user1, post2)
influx_client.upvote_post(user1, post1)
top_posts = influx_client.get_top_n_upvoted_post("7d", n=2)
for post in top_posts:
    print(f"Post {post['post_id']} has {post['upvotes']} upvotes.")

def createpost(posttitle, postdescription, postuser, postfilepath, postfilename):
    # insert SQL entry here inserting the post

    post = 1
    influx_client.create_post(postuser,post)
    BlobOperations.query1_createfile(postfilepath, postfilename)

def getposts():
    recent_posts = influx_client.get_top_n_upvoted_post("1d", 10)
    for post in recent_posts:
        print(f"Post: {post['post)id']}")

def detailpost(post_id):
    # SQL Query to get the post id

    #post = 
    # the syntax below shall be changed once we have the sql object
    BlobOperations.query3_getbloburl(post.filename)

    ## insert print statements here

def deletepost(post_id, user_id):
    # SQL Query Here for the object
    #post = 

    influx_client.delete_post(user_id,post_id)
    BlobOperations.query4_deleteblob(post.filename)

    # Once these are deleted, delete the sql entry
    
    print("Post {post.id} Deleted")

def editpost(post_id, posttitle, postdescription, postuser, postfilepath, postfilename):
    # sql query to get the current file's name if any
    # post = 

    if postfilename != None and postfilepath != None:  
      if post.filename:
          BlobOperations.query5_editblob(post.filename, postfilepath, postfilename)
      else:
          BlobOperations.query1_createfile(postfilepath, postfilename)

def upvote_post(post_id, user_id, vote):
    # sql logic here

    influx_client.upvote_post(user_id, post_id)
    
