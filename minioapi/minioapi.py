import json

from minio import Minio, ResponseError

from config import Config, Logger


class MinioApi():
    def __init__(self):
        self.logger = Logger.logger

        self.minioClient = Minio(
            endpoint=Config.minio_host,
            access_key=Config.minio_access_key,
            secret_key=Config.minio_secret_key,
            secure=True
        )

    def create_bucket(self, bucket_name):
        """
        Creates a bucket and set location to eu-west-1 on default.
        """
        if not self.minioClient.bucket_exists(bucket_name):
            self.logger.info("Create bucket {}".format(bucket_name))
            self.minioClient.make_bucket(bucket_name, location="eu-west-1")
        else:
            self.logger.warn("Bucket '{}' already exists.".format(bucket_name))

    def remove_bucket(self, name):
        """
        Removes a bucket by its name.
        """
        if self.minioClient.bucket_exists(name):
            self.logger.info("Remove bucket {}".format(name))
            self.minioClient.remove_bucket(name)
        else:
            self.logger.error("Bucket '{}' does not exist.".format(name))

    def list_objects_in_bucket(self, bucket_name):
        """
        Return a list of objects within a bucket.
        """
        return self.minioClient.list_objects(bucket_name, prefix=None, recursive=False)

    def upload_file(self, bucket_name, filename, file):
        """
        Uploads a file to a given bucket.
        """
        try:
            self.minioClient.fput_object(bucket_name, object_name=filename, file_path=file)
        except ResponseError as err:
            self.logger.error(err)

    def make_public(self, bucket_name):
        policy_read_only = {
            "Version": "2012-10-17", "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": ["*"]
                    },
                    "Action": ["s3:GetBucketLocation", "s3:ListBucket"],
                    "Resource": ["arn:aws:s3:::{}".format(bucket_name)]},
                {
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": ["*"]
                    },
                    "Action": ["s3:GetObject"],
                    "Resource": ["arn:aws:s3:::{}/*".format(bucket_name)]}]
        }
        self.minioClient.set_bucket_policy(bucket_name, json.dumps(policy_read_only))

    def get_public_url(self, bucket_name, object_name):
        url = self.minioClient.presigned_url(
            method='GET',
            bucket_name=bucket_name,
            object_name=object_name
        )
        # Extract public url.
        return url.split('?')[0]
