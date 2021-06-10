## lopco-http-adapter

Upload files via HTTP. Creates a job via the [lopco-job-manager](https://github.com/PlatonaM/lopco-job-manager) if a file is received.

### Configuration

`CONF_LOGGER_LEVEL`: Set logging level to `info`, `warning`, `error`, `critical` or `debug`.

`CONF_JM_URL`: URL of job manager.

`CONF_JM_API`: Job manager endpoint.

`CONF_DS_PATH`: Path to LOPCO data cache volume.

`CONF_DS_CHUNK_SIZE`: Chunk size for saving files.

### Ports

`port`: Port the protocol adapter will listen on.

`protocol`: Set protocol used by the port (`tcp`).

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

    # returns a SHA-512 checksum and a job ID as JSON
    {
        "checksum": "502a515f3b0c661ae0532da64863157a4e7c2b908351a15de1e59dc6fa0327ed695a9708ebaf312a1dd70617b573af6b52f45a380ccb29a3104f85560a102477",
        "job_id": "UVpxMTeqgMijLlbmNI8A_A"
    }
    
