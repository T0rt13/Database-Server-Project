from influx_cmds import DBInflux

# Example for influx
influx_client = DBInflux()
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