import React, { useState, Fragment } from 'react';
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
            `/add-post?categories=${form.categories}&title=${form.title}&body=${form.body}`,
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
            setSuccess(
                <a className="success-overlay" href="/viewall/posts">
                    Success! View here
                </a>
            );
            setError('');
        } else {
            setError(data.value);
        }
    };

    const onChange = (e) => {
        const input = e.currentTarget.value;
        const name = e.currentTarget.name;
        let formValue = { [name]: input };

        setForm((prevState) => {
            if (name === 'categories' && prevState.categories) {
                formValue = { [name]: [prevState.categories, input]}
            }
            return { ...prevState, ...formValue };
        });
    };

    const onFocus = () => {
        setError('');
    };

    return (
        <div className="post-form-container">
            {success && success}
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
                    <Query query={GET_CATEGORIES}>
                        {({ loading, error, data }) => {
                            if (loading) return <p>Loading...</p>;
                            if (error) return <p>Error</p>;
                            return data.allCategories.edges.map((cat) => (
                                <Fragment>
                                    <label htmlFor={cat.node.name}>{cat.node.name}</label>
                                    <input type="checkbox" name="categories" id={cat.node.name} label={cat.node.name} value={cat.node.name} onChange={onChange} />
                                </Fragment>
                            ));
                        }}
                    </Query>
                </div>
                <p className="error">{error}</p>
                <button className="btn btn-primary full-width">Add</button>
            </form>
        </div>
    );
};

export default AddPostForm;
