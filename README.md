# nginx-upstream-generator
Generates upstream routes config for a an Nginx load balancer

It's too much of a hassle to always type out Nginx config parameters. This script automates the process to return blocks like;
```
    # jellyfin-media_server
    upstream jellyfin-media_server {
        least_conn;
        server 10.0.1.41:8097;
        server 10.0.1.42:8097;
    }
    server {
        listen 8097;
        proxy_pass jellyfin-media_server;
    }
```

A ```conf.yaml``` file is OPTIONALLY needed in the same directory as the script to load the upstream servers

The script has also been compiled into a binary for portability.
