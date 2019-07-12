import React, { useState } from 'react';
import gql from 'graphql-tag';
import { Query } from 'react-apollo';

import './add-post-form.scss';

const GET_USERS = gql`
    {
        allUsers {
            edges {
                node {
                    username
                    uuid
                }
            }
        }
    }
`;

const GET_CATEGORIES = gql`
    {
        allCategories {
            edges {
                node {
                    name
                    colour
                }
            }
        }
    }
`;

const AddPostForm = () => {
    const [form, setForm] = useState({});
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const makeRequest = async (e) => {
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

        const data = await fetch(
            `/add-post?categories=${form.categories}&title=${form.title}&body=${form.body}&author=${
                form.author
            }`,
            settings
        )
            .then((response) => response.json())
            .then((json) => {
                return json;
            })
            .catch((e) => {
                setError(e);
            });

        if (data.value === 'success') {
            setSuccess(<a href="/viewall/posts">Success! View here</a>);
            setError('');

        } else {
            setError(data.value);
        }
    };

    const onChange = (e) => {
        const input = e.currentTarget.value;
        const name = e.currentTarget.name;
        const formValue = { [name]: input };
        setForm(prevState => {
            return { ...prevState, ...formValue };
        });
    };

    const onFocus = () => {
        setError('');
    };

    return (
        <div className="post-form-container">
            {success &&
                success
            }
            <form onSubmit={makeRequest}>
                <label className="hidden" for="name">
                    Add a new post
                </label>
                <div className="form-row">
                    <input
                        className="form-control"
                        type="text"
                        autocomplete="off"
                        onChange={onChange}
                        onFocus={onFocus}
                        placeholder="Title"
                        id="title"
                        value={form.title}
                        name="title"
                    />
                </div>
                <div className="form-row">
                    <textarea
                        className="form-control"
                        type="text"
                        autocomplete="off"
                        onChange={onChange}
                        onFocus={onFocus}
                        placeholder="Body"
                        id="body"
                        value={form.body}
                        name="body"
                    />
                </div>
                <div className="form-row">
                    <select
                        name={name}
                        className="form-control"
                        onChange={onChange}
                        onFocus={onFocus}
                        placeholder="author"
                        id="author"
                        value={form.author}
                        name="author">
                        <option disabled selected value="">Select an author</option>
                        <Query query={GET_USERS}>
                            {({ loading, error, data }) => {
                                if (loading) return <p>Loading...</p>;
                                if (error) return <p>Error</p>;
                                return data.allUsers.edges.map(user => (
                                    <option label={user.node.username} value={user.node.username} />
                                ))
                            }}
                        </Query>
                    </select>
                </div>
                <div className="form-row">
                    <select
                        name={name}
                        className="form-control"
                        onChange={onChange}
                        onFocus={onFocus}
                        placeholder="categories"
                        id="categories"
                        value={form.categories}
                        name="categories">
                        <option disabled selected value="">Select a category</option>
                        <Query query={GET_CATEGORIES}>
                            {({ loading, error, data }) => {
                                if (loading) return <p>Loading...</p>;
                                if (error) return <p>Error</p>;
                                return data.allCategories.edges.map(cat => (
                                    <option label={cat.node.name} value={cat.node.name} />
                                ))
                            }}
                        </Query>
                    </select>
                </div>
                <p className="error">{error}</p>
                <button className="btn btn-primary">Add</button>
            </form>
        </div>
    );
};

export default AddPostForm;
