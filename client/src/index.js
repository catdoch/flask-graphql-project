import React from 'react';
import ReactDOM from 'react-dom';

import App from './app.jsx';
import Post from './post.jsx';

const app = document.getElementById('app');
const post = document.getElementById('post');

if (app) {
    ReactDOM.render(<App />, app)
}

if (post) {
    ReactDOM.render(<Post />, post)
}
