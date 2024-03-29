# Migrating to V2

Much has changed with the new version, especially the management of the configuration file. Some fields have been added, while others have changed names, so first check that you have all the fields in the json with the correct name.

## New fields

Two new fields were introduced: `type` and `role` in the `client` and `users` sections, respectively.

The `type` field determines the type of torrent client you want to use(currently only qbittorrent is supported, so its value must be `qbittorrent`)

The `role` field, on the other hand, determines the role of a particular user. Currently there are 3 roles: 
- Reader
- Manager
- Administrator 

You can find more information [here](configuration_file/#enums)

## Changed names

There are 2 changes to the field names, the first is the name of the `qbittorrent` section which has been renamed to `client`. While the second is the `ip` field inside che `client` section which has been renamed to `host`

## Removed fileds

The `port` field has been removed from the `qbittorrent` section. This is due to the fact that I opted to use the `host` field to simultaneously enter the protocol(`http`/`https`), the ip address or the domain of qbittorrent and the port

## V1 vs V2
configurations in comparison

||| V1

```json
{
    "qbittorrent": {
        "ip": "192.168.178.102",
        "port": 8080,
        "user": "admin",
        "password": "admin"
    },
    "telegram": {
        "bot_token": "1111111:AAAAAAAA-BBBBBBBBB",
        "api_id": 1111,
        "api_hash": "aaaaaaaa"
    },

    "users": [
        {
            "user_id": 123456,
            "notify": false
        }
    ]
}
```

||| V2

```json
{
    "client": {
        "type": "qbittorrent",
        "host": "http://192.168.178.102:8080",
        "user": "admin",
        "password": "admin"
    },
    "telegram": {
        "bot_token": "1111111:AAAAAAAA-BBBBBBBBB",
        "api_id": 1111,
        "api_hash": "aaaaaaaa",
        "proxy": {
            "scheme": "http",
            "hostname": "myproxy.local",
            "port": 8080,
            "username": "admin",
            "password": "admin"
        }
    },

    "users": [
        {
            "user_id": 123456,
            "notify": false,
            "locale": "en",
            "role": "administrator"
        }
    ]
}
```
|||