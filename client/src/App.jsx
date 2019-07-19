import React, { useState, Fragment } from 'react';
import gql from 'graphql-tag';
import { Query } from 'react-apollo';

import './app.scss';

const App = () => {
    const [username, setUsername] = useState('');
    const [fetchError, setError] = useState('');
    const [sortBy, setSort] = useState('UUID_DESC');

    const GET_USERS = gql`
        query allUsers($sort: [UserObjectSortEnum]) {
            allUsers(sort: $sort) {
                edges {
                    node {
                        username
                        uuid
                        posts {
                            title
                        }
                    }
                }
            }
        }
    `;

    const addNewUser = async (e, refetch) => {
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
            .then((response) => response.json())
            .then((json) => {
                return json;
            })
            .catch((e) => {
                setError(e);
            });

        setUsername('');

        if (data.value === 'success') {
            refetch();
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

    const updateValue = (e, refetch) => {
        setSort(e.target.value);
        refetch();
    };

    return (
        <div className="user-container">
            <div className="user-subContainer">
                <Query query={GET_USERS} variables={{ sort: sortBy }}>
                    {({ loading, error, data, refetch }) => {
                        if (loading) return <p>Loading...</p>;
                        if (error) return <p>Error :(</p>;
                        return (
                            <div>
                                <form onSubmit={(e) => addNewUser(e, refetch)}>
                                    <label className="hidden" for="name">
                                        Add a new user
                                    </label>
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
                                        <p className="error">{fetchError}</p>
                                    </div>
                                    <button className="btn btn-primary">Add</button>
                                </form>
                                <div className="filter-box">
                                    <label htmlFor="sort-by">Sort By:</label>
                                    <select
                                        className="form-control"
                                        name="sort-by"
                                        onChange={(e) => updateValue(e, refetch)}
                                        value={sortBy}>
                                        <option value="UUID_DESC">User added descending</option>
                                        <option value="UUID_ASC">User added ascending</option>
                                        <option value="USERNAME_ASC">Username ascending</option>
                                        <option value="USERNAME_DESC">Username descending</option>
                                    </select>
                                </div>
                                {data.allUsers.edges.map((elem) => (
                                    <div className="user-post-container">
                                        <h2 className="block-value" key={elem.node.uuid}>
                                            {elem.node.username}
                                        </h2>
                                        {elem.node.posts && elem.node.posts.length > 0 && (
                                            <Fragment>
                                                <h3>{elem.node.username}'s post count:</h3>
                                                <p>{elem.node.posts.length}</p>
                                            </Fragment>
                                        )}
                                    </div>
                                ))}
                            </div>
                        );
                    }}
                </Query>
            </div>
        </div>
    );
};

export default App;
