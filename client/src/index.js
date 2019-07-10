import React from 'react';
import ReactDOM from 'react-dom';

import App from './App.jsx';
import Post from './Post.jsx';

const app = document.getElementById('app');
const post = document.getElementById('post');

if (app) {
    ReactDOM.render(<App />, app)
}

if (post) {
    ReactDOM.render(<Post />, post)
}
