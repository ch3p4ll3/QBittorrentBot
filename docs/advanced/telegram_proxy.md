# Configure proxy for Telegram

QBittorrent Bot can be configured to use a Telegram proxy to connect to the Telegram API. This can be useful if you are behind a firewall that blocks direct connections to Telegram.

To configure QBittorrent Bot to use a Telegram proxy, you will need to add a **proxy section** to the `config.json` file in the **telegram section**. The telegram section should have the following format:

```json5
"telegram": {
    "bot_token": "1111111:AAAAAAAA-BBBBBBBBB",
    "api_id": 1111,
    "api_hash": "aaaaaaaa",
    "proxy": {
        "scheme": "http", // http, sock4 or sock5
        "hostname": "myproxy.local",
        "port": 8080,
        "username": "admin",
        "password": "admin"
  }
}
```

Where:

- `scheme` is the protocol to use for the proxy connection. This can be `http`, `sock4` or `sock5`
- `hostname` is the hostname or IP address of the proxy server.
- `port` is the port number of the proxy server.
- `username` (optional) is the username for the proxy server.
- `password` (optional) is the password for the proxy server.

!!!
Once you have added the proxy section to the config.json file, you will need to restart QBittorrent Bot for the changes to take effect.
!!!