import React from 'react';
import ReactDOM from 'react-dom';
import { ApolloProvider } from 'react-apollo';
import ApolloClient, { gql } from 'apollo-boost';
import { InMemoryCache } from 'apollo-cache-inmemory';

const cache = new InMemoryCache();
const client = new ApolloClient({
    cache,
    uri: '/graphql'
});

import App from './App.jsx';
import Post from './Post.jsx';

const app = document.getElementById('app');
const post = document.getElementById('post');

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
    post);
}
