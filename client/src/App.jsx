import React, { useState, Fragment } from 'react';
import gql from 'graphql-tag';
import { Query } from 'react-apollo';

import './app.scss';

const GET_USERS = gql`
    {
        allUsers {
            edges {
                node {
                    username
                    uuid
                    posts {
                        edges {
                            node {
                                title
                            }
                        }
                    }
                }
            }
        }
    }
`;

const App = () => {
    const [username, setUsername] = useState('');
    const [fetchError, setError] = useState('');

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

    return (
        <div className="user-container">
            <div className="user-subContainer">
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
                <h2 className="block-title">View all users</h2>
                <Query query={GET_USERS}>
                    {({ loading, error, data, refetch }) => {
                        if (loading) return <p>Loading...</p>;
                        if (error) return <p>Error :(</p>;
                        return (
                            <div>
                                {data.allUsers.edges.map((elem) => (
                                    <div className="user-post-container">
                                        <h2 className="block-value" key={elem.node.uuid}>
                                            {elem.node.username}
                                        </h2>
                                        {elem.node.posts && elem.node.posts.edges.length > 0 && (
                                            <Fragment>
                                                <h3>{elem.node.username}'s Posts:</h3>
                                                {elem.node.posts.edges.map((post) => (
                                                    <p>{post.node.title}</p>
                                                ))}
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
