```python
import json
import os
import sys

class SimplePersistentKVStore:
    """
    A simple, single-file, persistent key-value store utility.
    It stores data in a dictionary and automatically persists changes to a JSON file.
    """

    def __init__(self, storage_file="kv_store.json"):
        """
        Initializes the key-value store.
        If the storage file exists, it loads the data from it.
        Otherwise, it starts with an empty store.

        Args:
            storage_file (str): The name of the JSON file to use for persistence.
        """
        self.storage_file = storage_file
        self._data = {}  # Internal dictionary to hold the key-value pairs
        self._load()     # Attempt to load existing data

    def _load(self):
        """
        Loads the data from the JSON storage file into the internal dictionary.
        If the file does not exist or is empty/corrupt, it initializes an empty dictionary.
        """
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    # Attempt to load JSON data; handle empty or malformed files
                    file_content = f.read().strip()
                    if file_content:
                        self._data = json.loads(file_content)
                    else:
                        self._data = {} # File exists but is empty
            except json.JSONDecodeError:
                print(f"Warning: Storage file '{self.storage_file}' is corrupt. Starting with an empty store.", file=sys.stderr)
                self._data = {}
            except Exception as e:
                print(f"Error loading data from '{self.storage_file}': {e}. Starting with an empty store.", file=sys.stderr)
                self._data = {}
        else:
            # If the file doesn't exist, start with an empty dictionary
            self._data = {}

    def _save(self):
        """
        Saves the current state of the internal dictionary to the JSON storage file.
        This method is called automatically after any modification (set, delete).
        """
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(self._data, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving data to '{self.storage_file}': {e}", file=sys.stderr)

    def set(self, key, value):
        """
        Sets a value for a given key. If the key already exists, its value is updated.
        The change is immediately persisted to the storage file.

        Args:
            key (str): The key to set. Must be a string.
            value: The value to associate with the key. Can be any JSON-serializable type.
        """
        if not isinstance(key, str):
            raise TypeError("Keys must be strings.")
        self._data[key] = value
        self._save()

    def get(self, key, default=None):
        """
        Retrieves the value associated with a given key.

        Args:
            key (str): The key to retrieve.
            default: The value to return if the key is not found. Defaults to None.

        Returns:
            The value associated with the key, or the default value if the key is not found.
        """
        return self._data.get(key, default)

    def delete(self, key):
        """
        Deletes a key-value pair from the store.
        The change is immediately persisted to the storage file.

        Args:
            key (str): The key to delete.

        Returns:
            The value that was deleted.

        Raises:
            KeyError: If the key does not exist in the store.
        """
        if key not in self._data:
            raise KeyError(f"Key '{key}' not found in the store.")
        value = self._data.pop(key)
        self._save()
        return value

    def clear(self):
        """
        Clears all key-value pairs from the store.
        The change is immediately persisted, resulting in an empty storage file.
        """
        self._data.clear()
        self._save()

    def keys(self):
        """
        Returns a view object that displays a list of all keys in the store.
        """
        return self._data.keys()

    def values(self):
        """
        Returns a view object that displays a list of all values in the store.
        """
        return self._data.values()

    def items(self):
        """
        Returns a view object that displays a list of a dictionary's key-value tuple pairs.
        """
        return self._data.items()

    def __len__(self):
        """
        Returns the number of key-value pairs in the store.
        """
        return len(self._data)

    def __contains__(self, key):
        """
        Checks if a key exists in the store.

        Args:
            key (str): The key to check.

        Returns:
            bool: True if the key exists, False otherwise.
        """
        return key in self._data

    def __str__(self):
        """
        Returns a string representation of the store's contents.
        """
        return str(self._data)

    def __repr__(self):
        """
        Returns a developer-friendly representation of the store.
        """
        return f"SimplePersistentKVStore(storage_file='{self.storage_file}', data={self._data})"


# --- Example Usage ---
if __name__ == "__main__":
    # Define a custom storage file for this example
    example_file = "my_app_data.json"

    print(f"--- Initializing KV Store ({example_file}) ---")
    # Initialize the store. It will load existing data or start fresh.
    store = SimplePersistentKVStore(storage_file=example_file)
    print(f"Current store content: {store}")
    print(f"Number of items: {len(store)}")

    print("\n--- Setting values ---")
    store.set("username", "alice_smith")
    store.set("last_login", "2023-10-27T10:30:00Z")
    store.set("is_active", True)
    store.set("settings", {"theme": "dark", "notifications": True})
    print(f"After setting values: {store}")

    print("\n--- Getting values ---")
    print(f"Username: {store.get('username')}")
    print(f"Last login: {store.get('last_login')}")
    print(f"User is active: {store.get('is_active')}")
    print(f"User settings: {store.get('settings')}")
    print(f"Non-existent key (default None): {store.get('non_existent_key')}")
    print(f"Non-existent key (default 'N/A'): {store.get('another_key', 'N/A')}")

    print("\n--- Checking key existence ---")
    print(f"'username' exists: {'username' in store}")
    print(f"'email' exists: {'email' in store}")

    print("\n--- Updating a value ---")
    store.set("last_login", "2023-10-27T11:45:00Z")
    print(f"Updated last login: {store.get('last_login')}")
    print(f"Store after update: {store}")

    print("\n--- Deleting a value ---")
    try:
        deleted_value = store.delete("is_active")
        print(f"Deleted 'is_active' with value: {deleted_value}")
        print(f"Store after deletion: {store}")
    except KeyError as e:
        print(e)

    print("\n--- Attempting to delete a non-existent key ---")
    try:
        store.delete("non_existent_key")
    except KeyError as e:
        print(f"Caught expected error: {e}")

    print("\n--- Iterating through keys and items ---")
    print("Keys:")
    for key in store.keys():
        print(f"- {key}")

    print("Items:")
    for key, value in store.items():
        print(f"- {key}: {value}")

    print(f"Number of items now: {len(store)}")

    print("\n--- Demonstrating persistence ---")
    print("Restarting the store (simulating a new run)...")
    # Create a new instance, which should load the data saved by the previous instance
    reloaded_store = SimplePersistentKVStore(storage_file=example_file)
    print(f"Reloaded store content: {reloaded_store}")
    print(f"Number of items in reloaded store: {len(reloaded_store)}")

    print("\n--- Clearing the store ---")
    reloaded_store.clear()
    print(f"Store after clearing: {reloaded_store}")
    print(f"Number of items after clearing: {len(reloaded_store)}")

    print("\n--- Verifying empty store after clear and reload ---")
    # Create another new instance to verify it's truly empty
    empty_store_check = SimplePersistentKVStore(storage_file=example_file)
    print(f"Reloaded store after clear: {empty_store_check}")
    print(f"Number of items: {len(empty_store_check)}")

    # Clean up the example file
    if os.path.exists(example_file):
        os.remove(example_file)
        print(f"\nCleaned up example file: {example_file}")
```