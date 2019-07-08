import React, { Component } from 'react';

class App extends Component {
    constructor(props) {
        super(props);

        this.state = {
            users: []
        }
    }

    componentDidMount() {
        this.getAllPosts();
    }

    async getAllPosts() {
        let response = await fetch('/getall');
        let users = await response.json();
        this.setState({ users });
    }

    render() {
        return (
            <div>
                <h1>View all users</h1>
                { this.state.users.map(users => (
                    <p key={users.uuid}>{users.username}</p>
                )) }
            </div>
        );
    }
}

export default App;