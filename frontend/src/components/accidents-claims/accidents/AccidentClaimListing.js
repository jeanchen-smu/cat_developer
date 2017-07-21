import React, { PropTypes } from "react";
import Paper from "material-ui/Paper";
import { Table, TableBody, TableHeader, TableHeaderColumn, TableRow, TableRowColumn } from "material-ui/Table";
import { Link } from "react-router";
import FloatingActionButton from "material-ui/FloatingActionButton";
import IconButton from "material-ui/IconButton";
import Fingerprint from "material-ui/svg-icons/action/fingerprint";
import Subheader from "material-ui/Subheader";
import { browserHistory } from "react-router";
import { grey500, blue800, white, black } from "material-ui/styles/colors";

const columns = ["Vehicle ID", "Date/Time", "Severity", "Type", "Claim No.", "Claim Amount", "Analyze"];

const styles = {
    editButton: {
        fill: grey500
    },
    table: {
        marginTop: 20
    },
    columns: {
        fields: {
            "Vehicle ID": {
                width: "10%"
            },
            "Date/Time": {
                width: "20%"
            },
            Severity: {
                width: "10%"
            },
            Type: {
                width: "10%"
            },
            "Claim No.": {
                width: "10%"
            },
            "Claim Amount": {
                width: "10%"
            },
            Analyze: {
                width: "10%"
            }
        }
    },
    iconButton: {
        color:blue800
    }
};

class AccidentClaimListing extends React.Component {
    constructor(props) {
        super(props);
        this.state = this.getDefaultState();
    }

    getDefaultState() {
        return {
            accidentClaims: []
        };
    }
    getAccidentClaims() {
        this.setState({
            accidentClaims: [
                {
                    "Vehicle ID": 37560,
                    "Date/Time": "2017-07-11T11:21:35.000+08:00",
                    Severity: "Heavy",
                    Type: "FRONT",
                    "Claim No.": "C123034",
                    "Claim Amount": 5400,
                    Analyze: ""
                },
                {
                    "Vehicle ID": 32560,
                    "Date/Time": "2017-05-15T10:10:35.000+08:00",
                    Severity: "Light",
                    Type: "REAR",
                    "Claim No.": "",
                    "Claim Amount": "",
                    Analyze: ""
                },
                {
                    "Vehicle ID": 35520,
                    "Date/Time": "2017-06-12T23:39:35.000+08:00",
                    Severity: "Heavy",
                    Type: "SIDE-HIT",
                    "Claim No.": "",
                    "Claim Amount": "",
                    Analyze: ""
                },
                {
                    "Vehicle ID": 27360,
                    "Date/Time": "2017-07-09T00:40:35.000+08:00",
                    Severity: "Heavy",
                    Type: "FRONT",
                    "Claim No.": "C133034",
                    "Claim Amount": 9050,
                    Analyze: ""
                }
            ]
        });
    }

    componentDidMount() {
        this.getAccidentClaims();
    }

    componentWillReceiveProps(nextProps) {
        this.getAccidentClaims();
    }

    analyzeAccident() {
        browserHistory.push("/home/accidentanalysis");
    }

    getHeader() {
        return (
            <TableHeader displaySelectAll={false} adjustForCheckbox={false}>
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
    getAnalyzeButton() {
        return (
            <IconButton
                iconStyle={styles.iconButton}
                onTouchTap={this.analyzeAccident.bind(this)}
            >
                <Fingerprint />
            </IconButton>
        );
    }
    getBody() {
        return (
            <TableBody displayRowCheckbox={false}>
                {this.state.accidentClaims.map((row, index) =>
                    <TableRow key={index}>
                        {columns.map(field =>
                            <TableRowColumn style={styles.columns.fields[field]} key={field}>
                                {field == "Analyze" ? this.getAnalyzeButton() : row[field]}
                            </TableRowColumn>
                        )}
                    </TableRow>
                )}
            </TableBody>
        );
    }

    render() {
        return (
            <Paper style={{ marginTop: 20 }}>
                <Subheader>List of accidents and claims(if any) for the selected period/vehicles</Subheader>
                <Table style={styles.table}>
                    {this.getHeader()}
                    {this.getBody()}
                </Table>
            </Paper>
        );
    }
}

export default AccidentClaimListing;
