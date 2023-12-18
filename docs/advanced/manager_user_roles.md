---
order: -20
---
# Managing users roles

QBittorrentBot provides a user role management system to control access to different actions and functionalities within the bot. The system defines three roles: Reader, Manager, and Admin, each with increasing permissions and capabilities.

## Reader

The Reader role grants basic access to view the list of active torrents and inspect the details of individual torrents. Users with the Reader role can view the torrent name, download speed, upload speed, progress, and file size. They can also view the category to which each torrent belongs.

## Manager

The Manager role extends the Reader role with additional permissions, allowing users to perform actions beyond mere observation. Manager-level users can download new torrents by sending magnet links or torrent files to the bot. They can also add or edit categories to organize their torrents effectively. Additionally, Manager users can set torrent priorities, enabling them to manage the download order and prioritize specific torrents. Moreover, they can pause or resume ongoing downloads, providing flexibility in managing their torrent activity.

## Admin

The Admin role, the most privileged, grants the user full control over the bot's functionalities. In addition to the capabilities of the Manager role, Admin users can remove torrents from their download lists, eliminating unwanted downloads. They can also remove categories, streamlining their torrent organization structure. And, as the highest-level role, Admin users have the authority to edit the bot's configuration files, modifying its settings and behavior.

This role management system ensures that users are granted access appropriate to their needs and responsibilities. Readers can observe and manage their torrent activity, Managers can perform more extensive actions, and Admins have full control over the bot's operation. This structure enhances security and prevents unauthorized users from modifying configuration files or deleting torrents.