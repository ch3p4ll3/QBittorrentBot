---
order: -10
---
# Add new entries in configuration file

Adding a new entry to the QBittorrentBot configuration file involves several steps:

- **Clone the repository**: `git clone https://github.com/ch3p4ll3/QBittorrentBot.git`

- **Navigate to the folder**: `src/configs`

- **Modify the pydantic class**:
        Identify the pydantic class where the new entry should be added.
        Add a new attribute to the class to represent the new entry.

- **Create a validation function (if necessary)**:
        If the new entry requires additional validation beyond the type provided by pydantic, create a validation function.
        The validation function should inspect the value of the new entry and check for any constraints or rules that need to be enforced.

- **Add the new entry to the config file**:
        Open the configuration file (usually `config.json`).
        Add a new property to the configuration object for the new entry.
        Set the value of the new property to the desired initial value.

- **Update the convert_type_from_string function (if necessary)**:
        If the new entry type requires a custom conversion from a string representation, add the conversion function to the `utils` file.
        The function should take a string representation of the new entry type and return the corresponding data type.

- **Update the bot code (if necessary)**:
        If the new entry is being used by the bot code, update the relevant parts of the code to handle the new entry type and its values.

- Build the docker image
- Start the docker container

You can now use the bot with the new entry, have fun🥳
