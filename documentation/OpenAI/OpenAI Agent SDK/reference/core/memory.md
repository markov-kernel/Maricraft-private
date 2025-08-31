---
title: Memory
source: https://openai.github.io/openai-agents-python/ref/memory/
---

# Memory

### Session

Bases: `Protocol`

Protocol for session implementations.

Session stores conversation history for a specific session, allowing
agents to maintain context without requiring explicit manual memory management.

Source code in `src/agents/memory/session.py`

|  |  |
| --- | --- |
| ```1516171819202122232425262728293031323334353637383940414243444546474849505152535455``` | ```md-code__content@runtime_checkableclass Session(Protocol):    """Protocol for session implementations.    Session stores conversation history for a specific session, allowing    agents to maintain context without requiring explicit manual memory management.    """    session_id: str    async def get_items(self, limit: int | None = None) -> list[TResponseInputItem]:        """Retrieve the conversation history for this session.        Args:            limit: Maximum number of items to retrieve. If None, retrieves all items.                   When specified, returns the latest N items in chronological order.        Returns:            List of input items representing the conversation history        """        ...    async def add_items(self, items: list[TResponseInputItem]) -> None:        """Add new items to the conversation history.        Args:            items: List of input items to add to the history        """        ...    async def pop_item(self) -> TResponseInputItem | None:        """Remove and return the most recent item from the session.        Returns:            The most recent item if it exists, None if the session is empty        """        ...    async def clear_session(self) -> None:        """Clear all items for this session."""        ...``` |

#### get\_items`async`

```
get_items(
    limit: int | None = None,
) -> list[TResponseInputItem]

```

Retrieve the conversation history for this session.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `limit` | `int | None` | Maximum number of items to retrieve. If None, retrieves all items.When specified, returns the latest N items in chronological order. | `None` |

Returns:

| Type | Description |
| --- | --- |
| `list[TResponseInputItem]` | List of input items representing the conversation history |

Source code in `src/agents/memory/session.py`

|  |  |
| --- | --- |
| ```2526272829303132333435``` | ```md-code__contentasync def get_items(self, limit: int | None = None) -> list[TResponseInputItem]:    """Retrieve the conversation history for this session.    Args:        limit: Maximum number of items to retrieve. If None, retrieves all items.               When specified, returns the latest N items in chronological order.    Returns:        List of input items representing the conversation history    """    ...``` |

#### add\_items`async`

```
add_items(items: list[TResponseInputItem]) -> None

```

Add new items to the conversation history.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `items` | `list[TResponseInputItem]` | List of input items to add to the history | _required_ |

Source code in `src/agents/memory/session.py`

|  |  |
| --- | --- |
| ```37383940414243``` | ```md-code__contentasync def add_items(self, items: list[TResponseInputItem]) -> None:    """Add new items to the conversation history.    Args:        items: List of input items to add to the history    """    ...``` |

#### pop\_item`async`

```
pop_item() -> TResponseInputItem | None

```

Remove and return the most recent item from the session.

Returns:

| Type | Description |
| --- | --- |
| `TResponseInputItem | None` | The most recent item if it exists, None if the session is empty |

Source code in `src/agents/memory/session.py`

|  |  |
| --- | --- |
| ```45464748495051``` | ```md-code__contentasync def pop_item(self) -> TResponseInputItem | None:    """Remove and return the most recent item from the session.    Returns:        The most recent item if it exists, None if the session is empty    """    ...``` |

#### clear\_session`async`

```
clear_session() -> None

```

Clear all items for this session.

Source code in `src/agents/memory/session.py`

|  |  |
| --- | --- |
| ```535455``` | ```md-code__contentasync def clear_session(self) -> None:    """Clear all items for this session."""    ...``` |

### SQLiteSession

Bases: `SessionABC`

SQLite-based implementation of session storage.

This implementation stores conversation history in a SQLite database.
By default, uses an in-memory database that is lost when the process ends.
For persistent storage, provide a file path.

Source code in `src/agents/memory/session.py`

|  |  |
| --- | --- |
| ```107108109110111112113114115116117118119120121122123124125126127128129130131132133134135136137138139140141142143144145146147148149150151152153154155156157158159160161162163164165166167168169170171172173174175176177178179180181182183184185186187188189190191192193194195196197198199200201202203204205206207208209210211212213214215216217218219220221222223224225226227228229230231232233234235236237238239240241242243244245246247248249250251252253254255256257258259260261262263264265266267268269270271272273274275276277278279280281282283284285286287288289290291292293294295296297298299300301302303304305306307308309310311312313314315316317318319320321322323324325326327328329330331332333334335336337338339340341342343344345346347348349350351352353354355356357358359360361362363364365366367368369``` | ```md-code__contentclass SQLiteSession(SessionABC):    """SQLite-based implementation of session storage.    This implementation stores conversation history in a SQLite database.    By default, uses an in-memory database that is lost when the process ends.    For persistent storage, provide a file path.    """    def __init__(        self,        session_id: str,        db_path: str | Path = ":memory:",        sessions_table: str = "agent_sessions",        messages_table: str = "agent_messages",    ):        """Initialize the SQLite session.        Args:            session_id: Unique identifier for the conversation session            db_path: Path to the SQLite database file. Defaults to ':memory:' (in-memory database)            sessions_table: Name of the table to store session metadata. Defaults to                'agent_sessions'            messages_table: Name of the table to store message data. Defaults to 'agent_messages'        """        self.session_id = session_id        self.db_path = db_path        self.sessions_table = sessions_table        self.messages_table = messages_table        self._local = threading.local()        self._lock = threading.Lock()        # For in-memory databases, we need a shared connection to avoid thread isolation        # For file databases, we use thread-local connections for better concurrency        self._is_memory_db = str(db_path) == ":memory:"        if self._is_memory_db:            self._shared_connection = sqlite3.connect(":memory:", check_same_thread=False)            self._shared_connection.execute("PRAGMA journal_mode=WAL")            self._init_db_for_connection(self._shared_connection)        else:            # For file databases, initialize the schema once since it persists            init_conn = sqlite3.connect(str(self.db_path), check_same_thread=False)            init_conn.execute("PRAGMA journal_mode=WAL")            self._init_db_for_connection(init_conn)            init_conn.close()    def _get_connection(self) -> sqlite3.Connection:        """Get a database connection."""        if self._is_memory_db:            # Use shared connection for in-memory database to avoid thread isolation            return self._shared_connection        else:            # Use thread-local connections for file databases            if not hasattr(self._local, "connection"):                self._local.connection = sqlite3.connect(                    str(self.db_path),                    check_same_thread=False,                )                self._local.connection.execute("PRAGMA journal_mode=WAL")            assert isinstance(self._local.connection, sqlite3.Connection), (                f"Expected sqlite3.Connection, got {type(self._local.connection)}"            )            return self._local.connection    def _init_db_for_connection(self, conn: sqlite3.Connection) -> None:        """Initialize the database schema for a specific connection."""        conn.execute(            f"""            CREATE TABLE IF NOT EXISTS {self.sessions_table} (                session_id TEXT PRIMARY KEY,                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP            )        """        )        conn.execute(            f"""            CREATE TABLE IF NOT EXISTS {self.messages_table} (                id INTEGER PRIMARY KEY AUTOINCREMENT,                session_id TEXT NOT NULL,                message_data TEXT NOT NULL,                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,                FOREIGN KEY (session_id) REFERENCES {self.sessions_table} (session_id)                    ON DELETE CASCADE            )        """        )        conn.execute(            f"""            CREATE INDEX IF NOT EXISTS idx_{self.messages_table}_session_id            ON {self.messages_table} (session_id, created_at)        """        )        conn.commit()    async def get_items(self, limit: int | None = None) -> list[TResponseInputItem]:        """Retrieve the conversation history for this session.        Args:            limit: Maximum number of items to retrieve. If None, retrieves all items.                   When specified, returns the latest N items in chronological order.        Returns:            List of input items representing the conversation history        """        def _get_items_sync():            conn = self._get_connection()            with self._lock if self._is_memory_db else threading.Lock():                if limit is None:                    # Fetch all items in chronological order                    cursor = conn.execute(                        f"""                        SELECT message_data FROM {self.messages_table}                        WHERE session_id = ?                        ORDER BY created_at ASC                    """,                        (self.session_id,),                    )                else:                    # Fetch the latest N items in chronological order                    cursor = conn.execute(                        f"""                        SELECT message_data FROM {self.messages_table}                        WHERE session_id = ?                        ORDER BY created_at DESC                        LIMIT ?                        """,                        (self.session_id, limit),                    )                rows = cursor.fetchall()                # Reverse to get chronological order when using DESC                if limit is not None:                    rows = list(reversed(rows))                items = []                for (message_data,) in rows:                    try:                        item = json.loads(message_data)                        items.append(item)                    except json.JSONDecodeError:                        # Skip invalid JSON entries                        continue                return items        return await asyncio.to_thread(_get_items_sync)    async def add_items(self, items: list[TResponseInputItem]) -> None:        """Add new items to the conversation history.        Args:            items: List of input items to add to the history        """        if not items:            return        def _add_items_sync():            conn = self._get_connection()            with self._lock if self._is_memory_db else threading.Lock():                # Ensure session exists                conn.execute(                    f"""                    INSERT OR IGNORE INTO {self.sessions_table} (session_id) VALUES (?)                """,                    (self.session_id,),                )                # Add items                message_data = [(self.session_id, json.dumps(item)) for item in items]                conn.executemany(                    f"""                    INSERT INTO {self.messages_table} (session_id, message_data) VALUES (?, ?)                """,                    message_data,                )                # Update session timestamp                conn.execute(                    f"""                    UPDATE {self.sessions_table}                    SET updated_at = CURRENT_TIMESTAMP                    WHERE session_id = ?                """,                    (self.session_id,),                )                conn.commit()        await asyncio.to_thread(_add_items_sync)    async def pop_item(self) -> TResponseInputItem | None:        """Remove and return the most recent item from the session.        Returns:            The most recent item if it exists, None if the session is empty        """        def _pop_item_sync():            conn = self._get_connection()            with self._lock if self._is_memory_db else threading.Lock():                # Use DELETE with RETURNING to atomically delete and return the most recent item                cursor = conn.execute(                    f"""                    DELETE FROM {self.messages_table}                    WHERE id = (                        SELECT id FROM {self.messages_table}                        WHERE session_id = ?                        ORDER BY created_at DESC                        LIMIT 1                    )                    RETURNING message_data                    """,                    (self.session_id,),                )                result = cursor.fetchone()                conn.commit()                if result:                    message_data = result[0]                    try:                        item = json.loads(message_data)                        return item                    except json.JSONDecodeError:                        # Return None for corrupted JSON entries (already deleted)                        return None                return None        return await asyncio.to_thread(_pop_item_sync)    async def clear_session(self) -> None:        """Clear all items for this session."""        def _clear_session_sync():            conn = self._get_connection()            with self._lock if self._is_memory_db else threading.Lock():                conn.execute(                    f"DELETE FROM {self.messages_table} WHERE session_id = ?",                    (self.session_id,),                )                conn.execute(                    f"DELETE FROM {self.sessions_table} WHERE session_id = ?",                    (self.session_id,),                )                conn.commit()        await asyncio.to_thread(_clear_session_sync)    def close(self) -> None:        """Close the database connection."""        if self._is_memory_db:            if hasattr(self, "_shared_connection"):                self._shared_connection.close()        else:            if hasattr(self._local, "connection"):                self._local.connection.close()``` |

#### \_\_init\_\_

```
__init__(
    session_id: str,
    db_path: str | Path = ":memory:",
    sessions_table: str = "agent_sessions",
    messages_table: str = "agent_messages",
)

```

Initialize the SQLite session.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `session_id` | `str` | Unique identifier for the conversation session | _required_ |
| `db_path` | `str | Path` | Path to the SQLite database file. Defaults to ':memory:' (in-memory database) | `':memory:'` |
| `sessions_table` | `str` | Name of the table to store session metadata. Defaults to'agent\_sessions' | `'agent_sessions'` |
| `messages_table` | `str` | Name of the table to store message data. Defaults to 'agent\_messages' | `'agent_messages'` |

Source code in `src/agents/memory/session.py`

|  |  |
| --- | --- |
| ```115116117118119120121122123124125126127128129130131132133134135136137138139140141142143144145146147148149150``` | ```md-code__contentdef __init__(    self,    session_id: str,    db_path: str | Path = ":memory:",    sessions_table: str = "agent_sessions",    messages_table: str = "agent_messages",):    """Initialize the SQLite session.    Args:        session_id: Unique identifier for the conversation session        db_path: Path to the SQLite database file. Defaults to ':memory:' (in-memory database)        sessions_table: Name of the table to store session metadata. Defaults to            'agent_sessions'        messages_table: Name of the table to store message data. Defaults to 'agent_messages'    """    self.session_id = session_id    self.db_path = db_path    self.sessions_table = sessions_table    self.messages_table = messages_table    self._local = threading.local()    self._lock = threading.Lock()    # For in-memory databases, we need a shared connection to avoid thread isolation    # For file databases, we use thread-local connections for better concurrency    self._is_memory_db = str(db_path) == ":memory:"    if self._is_memory_db:        self._shared_connection = sqlite3.connect(":memory:", check_same_thread=False)        self._shared_connection.execute("PRAGMA journal_mode=WAL")        self._init_db_for_connection(self._shared_connection)    else:        # For file databases, initialize the schema once since it persists        init_conn = sqlite3.connect(str(self.db_path), check_same_thread=False)        init_conn.execute("PRAGMA journal_mode=WAL")        self._init_db_for_connection(init_conn)        init_conn.close()``` |

#### get\_items`async`

```
get_items(
    limit: int | None = None,
) -> list[TResponseInputItem]

```

Retrieve the conversation history for this session.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `limit` | `int | None` | Maximum number of items to retrieve. If None, retrieves all items.When specified, returns the latest N items in chronological order. | `None` |

Returns:

| Type | Description |
| --- | --- |
| `list[TResponseInputItem]` | List of input items representing the conversation history |

Source code in `src/agents/memory/session.py`

|  |  |
| --- | --- |
| ```204205206207208209210211212213214215216217218219220221222223224225226227228229230231232233234235236237238239240241242243244245246247248249250251252253254255256257``` | ```md-code__contentasync def get_items(self, limit: int | None = None) -> list[TResponseInputItem]:    """Retrieve the conversation history for this session.    Args:        limit: Maximum number of items to retrieve. If None, retrieves all items.               When specified, returns the latest N items in chronological order.    Returns:        List of input items representing the conversation history    """    def _get_items_sync():        conn = self._get_connection()        with self._lock if self._is_memory_db else threading.Lock():            if limit is None:                # Fetch all items in chronological order                cursor = conn.execute(                    f"""                    SELECT message_data FROM {self.messages_table}                    WHERE session_id = ?                    ORDER BY created_at ASC                """,                    (self.session_id,),                )            else:                # Fetch the latest N items in chronological order                cursor = conn.execute(                    f"""                    SELECT message_data FROM {self.messages_table}                    WHERE session_id = ?                    ORDER BY created_at DESC                    LIMIT ?                    """,                    (self.session_id, limit),                )            rows = cursor.fetchall()            # Reverse to get chronological order when using DESC            if limit is not None:                rows = list(reversed(rows))            items = []            for (message_data,) in rows:                try:                    item = json.loads(message_data)                    items.append(item)                except json.JSONDecodeError:                    # Skip invalid JSON entries                    continue            return items    return await asyncio.to_thread(_get_items_sync)``` |

#### add\_items`async`

```
add_items(items: list[TResponseInputItem]) -> None

```

Add new items to the conversation history.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `items` | `list[TResponseInputItem]` | List of input items to add to the history | _required_ |

Source code in `src/agents/memory/session.py`

|  |  |
| --- | --- |
| ```259260261262263264265266267268269270271272273274275276277278279280281282283284285286287288289290291292293294295296297298299300301``` | ```md-code__contentasync def add_items(self, items: list[TResponseInputItem]) -> None:    """Add new items to the conversation history.    Args:        items: List of input items to add to the history    """    if not items:        return    def _add_items_sync():        conn = self._get_connection()        with self._lock if self._is_memory_db else threading.Lock():            # Ensure session exists            conn.execute(                f"""                INSERT OR IGNORE INTO {self.sessions_table} (session_id) VALUES (?)            """,                (self.session_id,),            )            # Add items            message_data = [(self.session_id, json.dumps(item)) for item in items]            conn.executemany(                f"""                INSERT INTO {self.messages_table} (session_id, message_data) VALUES (?, ?)            """,                message_data,            )            # Update session timestamp            conn.execute(                f"""                UPDATE {self.sessions_table}                SET updated_at = CURRENT_TIMESTAMP                WHERE session_id = ?            """,                (self.session_id,),            )            conn.commit()    await asyncio.to_thread(_add_items_sync)``` |

#### pop\_item`async`

```
pop_item() -> TResponseInputItem | None

```

Remove and return the most recent item from the session.

Returns:

| Type | Description |
| --- | --- |
| `TResponseInputItem | None` | The most recent item if it exists, None if the session is empty |

Source code in `src/agents/memory/session.py`

|  |  |
| --- | --- |
| ```303304305306307308309310311312313314315316317318319320321322323324325326327328329330331332333334335336337338339340341342``` | ```md-code__contentasync def pop_item(self) -> TResponseInputItem | None:    """Remove and return the most recent item from the session.    Returns:        The most recent item if it exists, None if the session is empty    """    def _pop_item_sync():        conn = self._get_connection()        with self._lock if self._is_memory_db else threading.Lock():            # Use DELETE with RETURNING to atomically delete and return the most recent item            cursor = conn.execute(                f"""                DELETE FROM {self.messages_table}                WHERE id = (                    SELECT id FROM {self.messages_table}                    WHERE session_id = ?                    ORDER BY created_at DESC                    LIMIT 1                )                RETURNING message_data                """,                (self.session_id,),            )            result = cursor.fetchone()            conn.commit()            if result:                message_data = result[0]                try:                    item = json.loads(message_data)                    return item                except json.JSONDecodeError:                    # Return None for corrupted JSON entries (already deleted)                    return None            return None    return await asyncio.to_thread(_pop_item_sync)``` |

#### clear\_session`async`

```
clear_session() -> None

```

Clear all items for this session.

Source code in `src/agents/memory/session.py`

|  |  |
| --- | --- |
| ```344345346347348349350351352353354355356357358359360``` | ```md-code__contentasync def clear_session(self) -> None:    """Clear all items for this session."""    def _clear_session_sync():        conn = self._get_connection()        with self._lock if self._is_memory_db else threading.Lock():            conn.execute(                f"DELETE FROM {self.messages_table} WHERE session_id = ?",                (self.session_id,),            )            conn.execute(                f"DELETE FROM {self.sessions_table} WHERE session_id = ?",                (self.session_id,),            )            conn.commit()    await asyncio.to_thread(_clear_session_sync)``` |

#### close

```
close() -> None

```

Close the database connection.

Source code in `src/agents/memory/session.py`

|  |  |
| --- | --- |
| ```362363364365366367368369``` | ```md-code__contentdef close(self) -> None:    """Close the database connection."""    if self._is_memory_db:        if hasattr(self, "_shared_connection"):            self._shared_connection.close()    else:        if hasattr(self._local, "connection"):            self._local.connection.close()``` |