### Description

    {
        "name": "HTTP Protocol Adapter",
        "image": "platonam/lopco-http-protocol-adapter:dev",
        "data_cache_path": "/data_cache",
        "description": "Upload files via HTTP.",
        "configs": {
            "CONF_LOGGER_LEVEL": "info"
        },
        "ports": [
            {
                "port": 80,
                "protocol": "tcp"
            }
        ]
    }

### API

#### /{machine-id}

**POST**

_Send a file to be processed by a pipeline._

    # Example

    curl --data-binary @machine_data.csv http://<host>/735d39eb6dc94acdadc9d019ff54fb1f
    502a515f3b0c661ae0532da64863157a4e7c2b908351a15de1e59dc6fa0327ed695a9708ebaf312a1dd70617b573af6b52f45a380ccb29a3104f85560a102477
