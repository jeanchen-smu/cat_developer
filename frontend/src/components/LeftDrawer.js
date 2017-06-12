import React, { PropTypes } from "react";
import Drawer from "material-ui/Drawer";
import { white, amber700 } from "material-ui/styles/colors";
import { Link } from "react-router";
import { List, ListItem } from "material-ui/List";

import Assessment from "material-ui/svg-icons/action/assessment";
import GpsFixed from "material-ui/svg-icons/device/gps-fixed";
import Timer from "material-ui/svg-icons/image/timer";
import PinDrop from "material-ui/svg-icons/maps/pin-drop";
import Grade from "material-ui/svg-icons/action/grade";


const styles = {
	logo: {
		padding: "15px 0 20px 15px",
		backgroundImage: "url(" + require("../images/fleet_man.png") + ")",
		height: 45,
		backgroundSize: "100% 100%"
	},
	listItem: {
		color: white,
		fontSize: 14
	},
	listIcon:{
		color:amber700
	}
};

class LeftDrawer extends React.Component {
	constructor() {
		super();
	}
	makeMenu() {
		return (
			<List>
				<ListItem
					key={1}
					primaryText="Overview"
					style={styles.listItem}
					leftIcon={<Assessment color={styles.listIcon.color} />}
					containerElement={<Link to={"/home/dashboard"} />}
				/>
				<ListItem
					key={2}
					primaryText="Tracking"
					style={styles.listItem}
					leftIcon={<GpsFixed color={styles.listIcon.color}/>}
					containerElement={<Link to={"/home/tracking"} />}
				/>
				<ListItem
					key={3}
					primaryText="Rankings"
					style={styles.listItem}
					leftIcon={<Grade color={styles.listIcon.color}/>}
					containerElement={<Link to={"/home/rank"} />}
				/>
			</List>
		);
	}

	render() {
		let { navDrawerOpen } = this.props;
		return (
			<Drawer docked={true} open={navDrawerOpen}>
				<div style={styles.logo} />
				{this.makeMenu()}
			</Drawer>
		);
	}
}

LeftDrawer.propTypes = {
	navDrawerOpen: PropTypes.bool,
	menus: PropTypes.array,
	username: PropTypes.string
};

export default LeftDrawer;