import React, { useState, useEffect } from 'react';
import './UsersTables.css';

// API Functions
const fetchPostgresUsers = async (searchQuery = '') => {
  const url = searchQuery.length >= 3 
    ? `http://127.0.0.1:8000/postgres/users?search_query=${encodeURIComponent(searchQuery)}`
    : 'http://127.0.0.1:8000/postgres/users';
  const response = await fetch(url);
  return await response.json();
};

const fetchFirebaseUsers = async (searchQuery = '') => {
  const url = searchQuery.length >= 3 
    ? `http://127.0.0.1:8000/firebase/users?search_query=${encodeURIComponent(searchQuery)}`
    : 'http://127.0.0.1:8000/firebase/users';
  const response = await fetch(url);
  return await response.json();
};

const addUserToPostgres = async () => {
  const response = await fetch('http://127.0.0.1:8000/postgres/users', {
    method: 'POST',
  });
  return await response.json();
};

const addUserToFirebase = async () => {
  const response = await fetch('http://127.0.0.1:8000/firebase/users', {
    method: 'POST',
  });
  return await response.json();
};

const deleteUserFromPostgres = async (userId) => {
  const response = await fetch(`http://127.0.0.1:8000/postgres/users/${userId}`, {
    method: 'DELETE',
  });
  return await response.json();
};

const deleteUserFromFirebase = async (userId) => {
  const response = await fetch(`http://127.0.0.1:8000/firebase/users/${userId}`, {
    method: 'DELETE',
  });
  return await response.json();
};

const syncPostgresToFirebase = async () => {
  const response = await fetch('http://127.0.0.1:8000/sync/postgres-to-firebase', {
    method: 'POST',
  });
  return await response.json();
};

const syncFirebaseToPostgres = async () => {
  const response = await fetch('http://127.0.0.1:8000/sync/firebase-to-postgres', {
    method: 'POST',
  });
  return await response.json();
};

const SearchBar = ({ onSearch, isLoading }) => {
  const [searchValue, setSearchValue] = useState('');
  const [error, setError] = useState('');

  const handleSearch = () => {
    if (searchValue.length > 0 && searchValue.length < 3) {
      setError('Search query must be at least 3 characters');
      return;
    }
    setError('');
    onSearch(searchValue);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  const handleClear = () => {
    setSearchValue('');
    setError('');
    onSearch('');
  };

  return (
    <div className="search-container">
      <div className="search-input-wrapper">
        <input
          type="text"
          className="search-input"
          value={searchValue}
          onChange={(e) => setSearchValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Search users..."
          disabled={isLoading}
        />
        {searchValue && (
          <button 
            className="search-clear-button"
            onClick={handleClear}
            disabled={isLoading}
          >
            ×
          </button>
        )}
      </div>
      <button 
        className="search-button"
        onClick={handleSearch}
        disabled={isLoading}
      >
        Search
      </button>
      {error && <div className="search-error">{error}</div>}
    </div>
  );
};

const LoadingSpinner = () => (
  <div className="loading-spinner">
    <div className="spinner"></div>
  </div>
);

const sortUsers = (users) => {
  return [...users].sort((a, b) => {
    const nameCompare = a.name.localeCompare(b.name);
    if (nameCompare !== 0) return nameCompare;
    return a.email.localeCompare(b.email);
  });
};

const UserTable = ({ users, title, onDelete, onAdd, userIdKey, isLoading, isAnyOperationInProgress }) => {
  const sortedUsers = sortUsers(users);

  return (
    <div className="table-container">
      <h1 className="table-title">{title}</h1>
      <div className="table-wrapper">
        {isLoading ? (
          <LoadingSpinner />
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {sortedUsers.map((user) => (
                <tr key={user[userIdKey]}>
                  <td>{user.name}</td>
                  <td>{user.email}</td>
                  <td>
                    <button 
                      className="delete-button"
                      onClick={() => onDelete(user[userIdKey])}
                      disabled={isAnyOperationInProgress}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
              {sortedUsers.length === 0 && (
                <tr>
                  <td colSpan="3" className="no-results">No users found</td>
                </tr>
              )}
            </tbody>
          </table>
        )}
      </div>
      <button 
        className="add-button" 
        onClick={onAdd}
        disabled={isAnyOperationInProgress}
      >
        {isAnyOperationInProgress ? 'Processing...' : `Add User to ${title}`}
      </button>
    </div>
  );
};

const UsersTables = () => {
  const [postgresUsers, setPostgresUsers] = useState([]);
  const [firebaseUsers, setFirebaseUsers] = useState([]);
  const [isInitialLoading, setIsInitialLoading] = useState(true);
  const [postgresOperation, setPostgresOperation] = useState(false);
  const [firebaseOperation, setFirebaseOperation] = useState(false);
  const [isSyncing, setIsSyncing] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const isAnyOperationInProgress = postgresOperation || firebaseOperation || isSyncing || isInitialLoading;

  const fetchUsers = async (query = '') => {
    try {
      setIsInitialLoading(true);
      const [pgUsers, fbUsers] = await Promise.all([
        fetchPostgresUsers(query),
        fetchFirebaseUsers(query)
      ]);
      setPostgresUsers(pgUsers);
      setFirebaseUsers(fbUsers);
    } catch (error) {
      console.error('Error fetching users:', error);
    } finally {
      setIsInitialLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleSearch = async (query) => {
    setSearchQuery(query);
    await fetchUsers(query);
  };

  const handlePostgresDelete = async (userId) => {
    try {
      setPostgresOperation(true);
      await deleteUserFromPostgres(userId);
      await fetchUsers(searchQuery);
    } finally {
      setPostgresOperation(false);
    }
  };

  const handleFirebaseDelete = async (userId) => {
    try {
      setFirebaseOperation(true);
      await deleteUserFromFirebase(userId);
      await fetchUsers(searchQuery);
    } finally {
      setFirebaseOperation(false);
    }
  };

  const handlePostgresAdd = async () => {
    try {
      setPostgresOperation(true);
      await addUserToPostgres();
      await fetchUsers(searchQuery);
    } finally {
      setPostgresOperation(false);
    }
  };

  const handleFirebaseAdd = async () => {
    try {
      setFirebaseOperation(true);
      await addUserToFirebase();
      await fetchUsers(searchQuery);
    } finally {
      setFirebaseOperation(false);
    }
  };

  const handleSyncPostgresToFirebase = async () => {
    try {
      setIsSyncing(true);
      await syncPostgresToFirebase();
      await fetchUsers(searchQuery);
    } finally {
      setIsSyncing(false);
    }
  };

  const handleSyncFirebaseToPostgres = async () => {
    try {
      setIsSyncing(true);
      await syncFirebaseToPostgres();
      await fetchUsers(searchQuery);
    } finally {
      setIsSyncing(false);
    }
  };

  return (
    <div className="user-tables">
      <SearchBar 
        onSearch={handleSearch} 
        isLoading={isAnyOperationInProgress}
      />
      <div className="tables-wrapper">
        <UserTable
          users={postgresUsers}
          title="PostgreSQL"
          onDelete={handlePostgresDelete}
          onAdd={handlePostgresAdd}
          userIdKey="user_id"
          isLoading={isInitialLoading}
          isAnyOperationInProgress={isAnyOperationInProgress}
        />
        
        <UserTable
          users={firebaseUsers}
          title="Firebase"
          onDelete={handleFirebaseDelete}
          onAdd={handleFirebaseAdd}
          userIdKey="uid"
          isLoading={isInitialLoading}
          isAnyOperationInProgress={isAnyOperationInProgress}
        />
      </div>

      <div className="sync-buttons">
        <button 
          className="sync-button" 
          onClick={handleSyncPostgresToFirebase}
          disabled={isAnyOperationInProgress}
        >
          {isSyncing ? 'Syncing...' : 'Sync PostgreSQL --> Firebase'}
        </button>
        <button 
          className="sync-button" 
          onClick={handleSyncFirebaseToPostgres}
          disabled={isAnyOperationInProgress}
        >
          {isSyncing ? 'Syncing...' : 'Sync PostgreSQL <-- Firebase'}
        </button>
      </div>
    </div>
  );
};

export default UsersTables;