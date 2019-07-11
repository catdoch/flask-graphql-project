import React, { useEffect, useState } from 'react';

import './post.scss';

const Post = () => {
    const [posts, setPosts] = useState([]);

    useEffect(() => {
        getAllPosts();
    }, []);

    const getAllPosts = async () => {
        const response = await fetch('/getall/posts');
        const posts = await response.json();
        setPosts(posts);
    };

    return (
        <div className="post-container">
                {posts.map((post) => (
                    <div className="post">
                        <header className="post-title">
                            <h3>{post.title} </h3>
                            { post.author && post.author.username &&
                                <p> {post.author.username}</p>
                            }
                        </header>
                        { post.categories && post.categories.length > 0 &&
                            post.categories.map(cat => (
                                <span style={{ backgroundColor: cat.colour }}>{ cat.name }</span>
                            ))
                        }
                        {post.body && <p>{post.body}</p> }
                    </div>
                ))}
        </div>
    );
};

export default Post;
