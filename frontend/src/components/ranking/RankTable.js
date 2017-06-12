import React, { PropTypes } from "react";
import {
	Table,
	TableBody,
	TableHeader,
	TableHeaderColumn,
	TableRow,
	TableRowColumn
} from "material-ui/Table";
import { Link } from "react-router";
import FloatingActionButton from "material-ui/FloatingActionButton";
import ContentCreate from "material-ui/svg-icons/content/create";
import { grey500, white, black} from "material-ui/styles/colors";
//import { typography } from "material-ui/styles";

const columns = [
	"Rank",
	"Vehicle ID",
	"Kind",
	"Score",
	"Max Overspeed",
	"Driving Time",
	"Distance"
];

const styles = {
	editButton: {
		fill: grey500
	},
	columns: {
		overall: {
			backgroundColor: black
		},
		fields: {
			Rank: {
				width: "10%"
			},
			"Vehicle ID": {
				width: "10%"
			},
			Kind: {
				width: "10%"
			},
			Score: {
				width: "10%"
			},
			"Max Overspeed": {
				width: "10%"
			},
			"Driving Time": {
				width: "10%"
			},
			Distance: {
				width: "10%"
			}
		}
	}
};

class RankTable extends React.Component {
	constructor() {
		super();
	}

	getHeader() {
		return (
			<TableHeader style={styles.columns.overall} displaySelectAll={false} adjustForCheckbox={false}>
				<TableRow>
					{columns.map(field =>
						<TableHeaderColumn style={styles.columns.fields[field]} key={field}>
							{field}
						</TableHeaderColumn>
					)}
				</TableRow>
			</TableHeader>
		);
	}

	getBody() {
		return (
			<TableBody displayRowCheckbox={false}>
				{this.props.rankingData.map((row, index) =>
					<TableRow key={index}>
						{columns.map(field =>
							<TableRowColumn style={styles.columns.fields[field]} key={field}>
								{row[field]}
							</TableRowColumn>
						)}
					</TableRow>
				)}
			</TableBody>
		);
	}

	render() {
		return (
			<Table>
				{this.getHeader()}
				{this.getBody()}
			</Table>
		);
	}
}

RankTable.propTypes = {
	rankingData: PropTypes.array
};

export default RankTable;
