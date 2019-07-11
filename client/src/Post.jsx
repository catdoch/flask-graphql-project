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

const Post = () => {
    // const [posts, setPosts] = useState([]);

    // useEffect(() => {
    //     getAllPosts();
    // }, []);

    // const getAllPosts = async () => {
    //     const response = await fetch('/getall/posts');
    //     const posts = await response.json();
    //     setPosts(posts);
    // };

    return (
        <div className="post-container">
            <Query query={GET_POSTS}>
                {({ loading, error, data }) => {
                    if (loading) return <p>Loading...</p>
                    if (error) return <p>Error :(</p>
                    return (
                        data.allPosts.edges.map(elem => (
                            <div className="post">
                                <header className="post-title">
                                    <h3>{elem.node.title} </h3>
                                    {elem.node.author && elem.node.author.username && <p> {elem.node.author.username}</p>}
                                </header>
                                {elem.node.categories &&
                                    elem.node.categories.edges.length > 0 &&
                                    elem.node.categories.edges.map((cat) => (
                                        <span style={{ backgroundColor: cat.node.colour }}>{cat.node.name}</span>
                                    ))}
                                {elem.node.body && <p>{elem.node.body}</p>}
                            </div>
                        )))
                }}
            </Query>



            {/* {posts.map((post) => (
                <div className="post">
                    <header className="post-title">
                        <h3>{post.title} </h3>
                        {post.author && post.author.username && <p> {post.author.username}</p>}
                    </header>
                    {post.categories &&
                        post.categories.length > 0 &&
                        post.categories.map((cat) => (
                            <span style={{ backgroundColor: cat.colour }}>{cat.name}</span>
                        ))}
                    {post.body && <p>{post.body}</p>}
                </div>
            ))} */}
        </div>
    );
};

export default Post;
