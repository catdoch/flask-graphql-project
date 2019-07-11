import React, { useEffect, useState } from 'react';
import gql from 'graphql-tag';
import { Query } from 'react-apollo';

import './post.scss';

const GET_POSTS = gql`
    {
        allPosts {
            edges {
                node {
                    author {
                        username
                        uuid
                    }
                    title
                    body
                    categories {
                        edges {
                            node {
                                name
                                colour
                            }
                        }
                    }
                }
            }
        }
    }
`;

const Post = () => (
    <div className="post-container">
        <Query query={GET_POSTS}>
            {({ loading, error, data }) => {
                if (loading) return <p>Loading...</p>;
                if (error) return <p>Error :(</p>;
                return data.allPosts.edges.map((elem) => (
                    <div className="post">
                        <header className="post-title">
                            <h3>{elem.node.title} </h3>
                            {elem.node.author && elem.node.author.username && (
                                <p> {elem.node.author.username}</p>
                            )}
                        </header>
                        {elem.node.categories &&
                            elem.node.categories.edges.length > 0 &&
                            elem.node.categories.edges.map((cat) => (
                                <span style={{ backgroundColor: cat.node.colour }}>
                                    {cat.node.name}
                                </span>
                            ))}
                        {elem.node.body && <p>{elem.node.body}</p>}
                    </div>
                ));
            }}
        </Query>
    </div>
);

export default Post;
