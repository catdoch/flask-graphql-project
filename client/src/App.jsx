import React, { useEffect, useState } from 'react';

import './app.scss';

const App = () => {
    const [users, setUsers] = useState([]);
    const [username, setUsername] = useState('');
    const [error, setError] = useState('');

    useEffect(() => {
        getAllUsers();
    }, []);

    const getAllUsers = async () => {
        let response = await fetch('/getall/users');
        let users = await response.json();
        setUsers(users.users);
    };

    const addNewUser = async (e) => {
        e.preventDefault();

        const settings = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            mode: 'cors',
            cache: 'no-cache',
            credentials: 'same-origin',
        };

        const data = await fetch(`/add-user?username=${username}`, settings)
            .then(response => response.json())
            .then(json => {
                return json;
            })
            .catch(e => {
                setError(e);
            });

        setUsername('');

        if (data.value === 'success') {
            getAllUsers();
            setError('');
        } else {
            setError(data.value);
        }
    };

    const onChange = (e) => {
        const input = e.currentTarget.value;
        setUsername(input);
    };

    const onFocus = () => {
        setError('');
    };

    return (
        <div className="user-container">
            <div className="user-subContainer">
                <h2 className="block-title">View all users</h2>
                {users.map((user) => (
                    <p className="block-value" key={user.uuid}>
                        {user.username}
                    </p>
                ))}
            </div>
            <div className="user-subContainer">
                <h2 className="block-title block-right">Or... add a new user</h2>
                <form onSubmit={addNewUser}>
                    <label className="hidden" for="name">Add a new user</label>
                    <div className="form-row">
                        <input
                            className="form-control"
                            type="text"
                            autocomplete="off"
                            onChange={onChange}
                            onFocus={onFocus}
                            placeholder="Enter you username"
                            id="name"
                            value={username}
                            name="name"
                        />
                        <p className="error">{error}</p>
                    </div>
                    <button className="btn btn-primary">Add</button>
                </form>
            </div>
        </div>
    );
};

export default App;
