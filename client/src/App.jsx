import React, { useEffect, useState } from 'react';

import './app.scss';

const App = () => {
    const [users, setUsers] = useState([]);
    const [username, setUsername] = useState('');

    useEffect(() => {
        getAllUsers();
    }, []);

    const getAllUsers = async () => {
        let response = await fetch('/getall');
        let users = await response.json();
        setUsers(users);
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
                return e
            });

        if (data.value === 'success') {
            getAllUsers();
            setUsername('');
        }
    };

    const onChange = (e) => {
        const input = e.currentTarget.value;
        setUsername(input);
    }

    return (
        <div className="user-container">
            <div className="user-subContainer">
                <h2 className="block-title">View all users</h2>
                {users.map((users) => (
                    <p className="block-value" key={users.uuid}>
                        {users.username}
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
                            onChange={onChange}
                            placeholder="Enter you username"
                            id="name"
                            value={username}
                            name="name"
                        />
                    </div>
                    <button className="btn btn-primary">Add</button>
                </form>
            </div>
        </div>
    );
};

export default App;
