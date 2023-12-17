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