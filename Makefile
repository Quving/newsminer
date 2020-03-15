lda:
	docker pull quving/newsminer:latest
	docker run -e --rm \
	    -e NEWSMINER_AUTH_TOKEN=$(NEWSMINER_AUTH_TOKEN) \
	    -e NEWSMINER_MINIO_ACCESS_KEY=$(NEWSMINER_MINIO_ACCESS_KEY) \
	    -e NEWSMINER_MINIO_SECRET_KEY=$(NEWSMINER_MINIO_SECRET_KEY) \
	    -e NEWSMINER_MINIO_HOST=$(NEWSMINER_MINIO_HOST) \
	    quving/newsminer:latest
