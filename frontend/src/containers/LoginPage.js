import React from "react";
import MuiThemeProvider from "material-ui/styles/MuiThemeProvider";
import Paper from "material-ui/Paper";
import RaisedButton from "material-ui/RaisedButton";
import FlatButton from "material-ui/FlatButton";
import Checkbox from "material-ui/Checkbox";
import { grey800, white } from "material-ui/styles/colors";
import Help from "material-ui/svg-icons/action/help";
import TextField from "material-ui/TextField";
import { Link } from "react-router";
import ThemeDefault from "../theme-default";
import axios from "axios";
import { browserHistory } from 'react-router';

const styles = {
    page: {
        backgroundImage: "url(" + require("../images/login_bg.jpg") + ")",
        height: "100%",
        backgroundPosition: "center",
        backgroundRepeat: "no-repeat",
        backgroundSize: "cover"
    },
    loginContainer: {
        minWidth: 320,
        maxWidth: 400,
        height: "auto",
        position: "absolute",
        top: "20%",
        left: 0,
        right: 0,
        margin: "auto"
    },
    paper: {
        padding: 20,
        overflow: "auto"
    },
    buttonsDiv: {
        textAlign: "center",
        padding: 10
    },
    flatButton: {
        color: grey800
    },
    checkRemember: {
        style: {
            float: "left",
            maxWidth: 180,
            paddingTop: 5
        },
        labelStyle: {
            color: grey800
        },
        iconStyle: {
            color: grey800,
            borderColor: grey800,
            fill: grey800
        }
    },
    loginBtn: {
        float: "right"
    },
    btn: {
        background: "#4f81e9",
        color: white,
        padding: 7,
        borderRadius: 2,
        margin: 2,
        fontSize: 13
    },
    btnFacebook: {
        background: "#4f81e9"
    },
    btnGoogle: {
        background: "#e14441"
    },
    btnSpan: {
        marginLeft: 5
    }
};

class LoginPage extends React.Component {
    constructor() {
        super();
        this.state = {
            username: "goldbell",
            password: "1234",
            uname_error_msg: "",
            pwd_error_msg: ""
        };
    }

    updateVals(event, val) {
        this.setState({ [event.target.name]: val, uname_error_msg:"", pwd_error_msg:"" });
    }

    validate() {
        var valid = true;
        if (this.state.username === "") {
            this.setState({ uname_error_msg: " " });
            valid = false;
        }

        if (this.state.password === "") {
            this.setState({ pwd_error_msg: " " });
            valid = false;
        }
        return valid;
    }
    getRequestObj() {
        return {
            method: "post",
            url: "/api/login",
            headers: {
                "Content-Type": "application/json"
            },
            data: {
                username: this.state.username,
                password: this.state.password
            }
        };
    }
	
	login(access_token){
		localStorage.setItem("access_token", access_token);
		browserHistory.push("/home");
	}

	refuse(msg){
        this.setState({ uname_error_msg: msg });
        this.setState({ pwd_error_msg: msg });
	}

    handleLogin() {
        //if (!this.validate()) return;

        axios(this.getRequestObj())
            .then(resp => {
				this.login(resp.data.access_token);
            })
            .catch(err => {
				this.refuse(" ");
            });
    }

    render() {
        return (
            <MuiThemeProvider muiTheme={ThemeDefault}>
                <div style={styles.page}>
                    <div style={styles.loginContainer}>
                        <Paper style={styles.paper}>
                            <div>
                                <TextField
                                    name="username"
                                    hintText="Username"
                                    floatingLabelText="Username"
                                    errorText={this.state.uname_error_msg}
                                    onChange={this.updateVals.bind(this)}
                                    fullWidth={true}
                                />
                                <TextField
                                    name="password"
                                    hintText="Password"
                                    floatingLabelText="Password"
                                    errorText={this.state.pwd_error_msg}
                                    onChange={this.updateVals.bind(this)}
                                    fullWidth={true}
                                    type="password"
                                />
                                <div>
                                    <RaisedButton
                                        type="submit"
                                        onTouchTap={this.handleLogin.bind(this)}
                                        label="Login"
                                        primary={true}
                                        style={styles.loginBtn}
                                    />
                                </div>
                            </div>
                        </Paper>

                        <div style={styles.buttonsDiv}>
                            <FlatButton
                                label="Forgot Password?"
                                style={styles.flatButton}
                                icon={<Help />}
                            />
                        </div>
                    </div>
                </div>
            </MuiThemeProvider>
        );
    }
}

export default LoginPage;
