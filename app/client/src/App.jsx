import React, { useState, Fragment } from 'react';
import gql from 'graphql-tag';
import { Query } from 'react-apollo';

import './app.scss';

const App = () => {
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
