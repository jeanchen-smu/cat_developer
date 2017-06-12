import React, { PropTypes } from "react";
import Drawer from "material-ui/Drawer";
import DatePicker from "material-ui/DatePicker";
import FloatingActionButton from "material-ui/FloatingActionButton";
import RaisedButton from "material-ui/RaisedButton";
//import FilterList from "material-ui/svg-icons/content/filter-list";
import HorizIcon from "material-ui/svg-icons/navigation/more-horiz";

import TextField from "material-ui/TextField";
import { typography } from "material-ui/styles";
import { white } from "material-ui/styles/colors";
//import * as moment from 'moment';

const styles = {
	button: {
		margin: 0,
		top: 65,
		right: 20,
		bottom: "auto",
		left: "auto",
		position: "fixed"
	},

	drawer: {
		backgroundColor: white,
		height: "calc(100% - 115px)",
		top: 115
	},

	filter: {
		container: {
			padding: 10
		},
		header: {
			paddingLeft: 10,
			paddingTop: 20,
			fontWeight: typography.textFullBlack
		},
		content: {
			paddingTop: 10,
			paddingLeft: 20,
			fontWeight: typography.textLightBlack
		},
		button: {
			margin: 12
		}
	}
};

class FilterDrawer extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			drawerOpen: false,
			filterObj: props.filterObj
		};
	}

	toggleDrawer() {
		this.setState({ drawerOpen: !this.state.drawerOpen });
	}

	setStartDate(event, dateObj) {
		let filterObj = this.state.filterObj;
		filterObj.startDate = dateObj;
		this.setState({ filterObj: filterObj });
	}

	setEndDate(event, dateObj) {
		let filterObj = this.state.filterObj;
		filterObj.endDate = dateObj;
		this.setState({ filterObj: filterObj });
	}

	setVehicleList(event) {
		let filterObj = this.state.filterObj;
		filterObj.vehicleList = [event.target.value];
		this.setState({ filterObj: filterObj });
	}

	applyFilter() {
		this.props.applyFilter(this.state.filterObj);
		this.setState({drawerOpen:false});
	}

	render() {
		return (
			<div>
				<div>
					<FloatingActionButton
						mini={true}
						style={styles.button}
						onTouchTap={this.toggleDrawer.bind(this)}
					>
						<HorizIcon />
					</FloatingActionButton>
				</div>
				<div>
					<Drawer
						width={300}
						openSecondary={true}
						open={this.state.drawerOpen}
						containerStyle={styles.drawer}
					>
						<div style={styles.filter.container}>
							<div style={styles.filter.header}>
								Date Filter
							</div>
							<div style={styles.filter.content}>
								<DatePicker
									defaultDate={this.state.filterObj.startDate}
									hintText="Start Date"
									container="inline"
									onChange={this.setStartDate.bind(this)}
								/>
								<DatePicker
									defaultDate={this.state.filterObj.endDate}
									hintText="End Date"
									container="inline"
									onChange={this.setEndDate.bind(this)}
								/>
							</div>
							<div style={styles.filter.header}>
								Vehicle Filter
							</div>
							<div style={styles.filter.content}>
								<TextField
									hintText="Vehicle ID"
									onChange={this.setVehicleList.bind(this)}
								/>
							</div>
							<div style={styles.filter.header}>
								<RaisedButton
									label="Apply"
									secondary={true}
									onTouchTap={this.applyFilter.bind(this)}
								/>
							</div>
						</div>
					</Drawer>
				</div>
			</div>
		);
	}
}

FilterDrawer.propTypes = {
	drawerOpen: PropTypes.bool,
	filterObj: PropTypes.object,
	applyFilter: PropTypes.func
};

/*filter object that should be passed to the Filter Component*/
class FilterObj {
	constructor() {
		this.startDate = null;
		(this.endDate = null), (this.vehicleList = []);
	}
}

export default FilterDrawer;
export { FilterObj };
