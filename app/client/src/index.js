import React from 'react';
import ReactDOM from 'react-dom';
import { ApolloProvider } from 'react-apollo';
import ApolloClient from 'apollo-boost';
import { InMemoryCache } from 'apollo-cache-inmemory';

const cache = new InMemoryCache();
const client = new ApolloClient({
    cache,
    uri: '/graphql',
});

import App from './App.jsx';
import Post from './Post.jsx';
import AddPostForm from './AddPostForm.jsx';

const app = document.getElementById('app');
const post = document.getElementById('post');
const addPostForm = document.getElementById('add-post-form');

if (app) {
    ReactDOM.render(
        <ApolloProvider client={client}>
            <App />
        </ApolloProvider>,
        app
    );
}

if (post) {
    ReactDOM.render(
        <ApolloProvider client={client}>
            <Post />
        </ApolloProvider>,
        post
    );
}

if (addPostForm) {
    ReactDOM.render(
        <ApolloProvider client={client}>
            <AddPostForm />
        </ApolloProvider>,
        addPostForm
    );
}
