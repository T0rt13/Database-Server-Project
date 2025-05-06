from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

class DBInflux:
    INFLUXDB_TOKEN="OQZvPOTqdOVgXCY-_uO72iDaKW9Pof70VGj3tI0KU-rRE7e51t7JqXg0wYITehHklrvsQfppsMj6teNWvtD8mg=="
    client = InfluxDBClient(url = "http://localhost:8086",org = "influx_org", token=INFLUXDB_TOKEN)
    write_api = client.write_api(write_options=SYNCHRONOUS) 
    query_api = client.query_api()
    bucket = 'bucket1'
        
    def __create_post_metrics_point(self, post_id, action, count):
        """
        Writes a metrics point to the "post_metrics" measurement in InfluxDB.

        Args:
            post_id (str): The unique identifier of the post.
            action (str): The action performed on the post (e.g., "create", "edit", "upvote").
            count (int): The count of the action performed (usually 1).

        Returns:
            None
        """
        point = (Point("post_metrics")
                 .tag("post_id", post_id)
                 .tag("action", action)
                 .field("count", count)
                 )
        self.write_api.write(bucket=self.bucket, record=point)
        
    def __create_user_metrics_point(self, user_id, action, post_id):
        """
        Writes a user-related metrics point to the "user_metrics" measurement in InfluxDB.

        Args:
            user_id (str): The unique identifier of the user.
            action (str): The action performed by the user (e.g., "create", "edit", "upvote").
            post_id (str): The unique identifier of the post associated with the action.

        Returns:
            None
        """
        point = ((Point("user_metrics")
                 .tag("user_id", user_id)
                 .tag("action", action)
                 .field("post_id", post_id)
                 ))
        self.write_api.write(bucket=self.bucket, record=point)
        
    def create_post(self, user_id, post_id):
        """
        Creates a new post and records its creation action for both the post and the user.

        Args:
            user_id (str): The unique identifier of the user who created the post.
            post_id (str): The unique identifier of the newly created post.

        Returns:
            None
        """
        self.__create_post_metrics_point(post_id,"create",1)
        self.__create_user_metrics_point(user_id,'create',post_id)
        
    def edit_post(self, user_id, post_id):
        """
        Records the editing action performed on an existing post.

        Args:
            user_id (str): The unique identifier of the user who edited the post.
            post_id (str): The unique identifier of the post being edited.

        Returns:
            None
        """
        self.__create_post_metrics_point(post_id,"edit",1)
        self.__create_user_metrics_point(user_id,'edit',post_id)
        
    def delete_post(self, user_id, post_id):
        """
        Records the deletion of a post and updates both the post and user metrics.

        Args:
            user_id (str): The unique identifier of the user who deleted the post.
            post_id (str): The unique identifier of the post being deleted.

        Returns:
            None
        """
        self.__create_post_metrics_point(post_id,"delete",1)
        self.__create_user_metrics_point(user_id,'delete',post_id)
        
    def upvote_post(self, user_id, post_id):
        """
        Records an upvote action on a post by a user.

        Args:
            user_id (str): The unique identifier of the user who upvoted the post.
            post_id (str): The unique identifier of the post being upvoted.

        Returns:
            None
        """
        self.__create_post_metrics_point(post_id, "upvote", 1)
        self.__create_user_metrics_point(user_id, "upvote", post_id)

    def get_top_n_upvoted_post(self, time_range="1d", n=1):
        """
        Retrieves the top `n` posts with the most upvotes within a given time range.

        Args:
            time_range (str): The time range for the query (e.g., "1d" for 1 day, "7d" for 7 days). Default is "1d".
            n (int): The number of top posts to return. Default is 1.

        Returns: list of dict: A list of dictionaries containing:
                - `post_id` (str): The ID of the post.
                - `upvotes` (int): The total number of upvotes the post has received.
                
            Example:
            ```python
            [{'post_id': 'abc123', 'upvotes': 15}]
            ```
        """
        query = f'''
        from(bucket: "{self.bucket}")
        |> range(start: -{time_range})
        |> filter(fn: (r) => r["_measurement"] == "post_metrics")
        |> filter(fn: (r) => r["action"] == "upvote")
        |> group(columns: ["post_id"])
        |> sum()
        |> keep(columns: ["post_id", "_value"])
        |> group()
        |> top(n: {n}, columns: ["_value"]) 
        '''
        tables = self.query_api.query(org="influx_org", query=query)
        results = []
        for table in tables:
            for record in table.records:
                results.append({
                    "post_id": record["post_id"],
                    "upvotes": int(record["_value"])
                })
        return results