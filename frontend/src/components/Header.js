import React, { PropTypes } from "react";
import AppBar from "material-ui/AppBar";
import IconButton from "material-ui/IconButton";
import MenuIcon from "material-ui/svg-icons/navigation/menu";
import ExitToAppIcon from "material-ui/svg-icons/action/exit-to-app";
import SettingsIcon from "material-ui/svg-icons/action/settings";
import { white } from "material-ui/styles/colors";
import { browserHistory } from 'react-router';

const styles = {
	appBar: {
		position: "fixed",
		top: 0,
		overflow: "hidden",
		maxHeight: 75
	},
	menuButton: {
		marginLeft: 10
	}
};

class Header extends React.Component {
	constructor() {
		super();
	}

    logOut(){
        localStorage.removeItem("token");
		browserHistory.push("/login");;
    }

	getLeftMenu() {
		return (
			<IconButton
				style={styles.menuButton}
				onClick={this.props.handleChangeRequestNavDrawer}
			>
				<MenuIcon color={white} />
			</IconButton>
		);
	}

	getRightMenu() {
		return (
			<div>
				<IconButton style={styles.menuButton}>
					<SettingsIcon color={white} />
				</IconButton>
				<IconButton style={styles.menuButton} onClick={this.logOut.bind(this)}>
					<ExitToAppIcon color={white} />
				</IconButton>
			</div>
		);
	}

	render() {
		return (
			<AppBar
				style={{ ...this.props.styles, ...styles.appBar }}
				iconElementLeft={this.getLeftMenu()}
				iconElementRight={this.getRightMenu()}
			/>
		);
	}
}

Header.propTypes = {
	styles: PropTypes.object,
	handleChangeRequestNavDrawer: PropTypes.func
};

export default Header;
