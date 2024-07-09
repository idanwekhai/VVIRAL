import mlflow

remote_server_uri = "http://127.0.0.1:5000"  # set to your server URI
mlflow.set_tracking_uri(remote_server_uri)
mlflow.set_experiment("/my-experiment")
with mlflow.start_run():
    mlflow.log_param("a", 1)
    mlflow.log_metric("b", 2)
