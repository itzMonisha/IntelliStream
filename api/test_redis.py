from cache import redis_client

redis_client.set(
    "project",
    "IntelliStream"
)

print(
    redis_client.get("project")
)