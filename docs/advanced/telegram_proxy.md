# Configure Proxy for Telegram

QBittorrent Bot can be configured to use a **Telegram proxy** to connect to the Telegram API. This is useful if you are behind a firewall or need to route traffic through a proxy to reach Telegram's servers.

To configure the bot to use a Telegram proxy, you need to add a **proxy section** under the `telegram` section in your `config.yml` file.

Here's an example of the updated `config.yml` format with proxy settings:

```yaml
telegram:
  bot_token: PUT_YOUR_TELEGRAM_BOT_TOKEN_HERE
  proxy:
    scheme: http     # Proxy protocol, can be "http", "socks4", or "socks5"
    hostname: myproxy.local   # Proxy server hostname or IP
    port: 8080       # Proxy server port
    username: admin  # Optional, username for proxy authentication
    password: admin  # Optional, password for proxy authentication
```

Where:

* **`scheme`**: The protocol to use for the proxy connection. Can be:

  * `http`
  * `socks4`
  * `socks5`

* **`hostname`**: The hostname or IP address of the proxy server.

* **`port`**: The port number of the proxy server.

* **`username`** (optional): The username for the proxy server (if authentication is required).

* **`password`** (optional): The password for the proxy server (if authentication is required).

!!!
Once you have added the proxy section to the `config.yml` file, you will need to restart QBittorrent Bot for the changes to take effect.
!!!