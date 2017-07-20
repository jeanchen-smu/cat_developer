import React from "react";
import { Card, CardHeader, CardText } from "material-ui/Card";
import {
    Table,
    TableBody,
    TableHeader,
    TableHeaderColumn,
    TableRow,
    TableRowColumn
} from "material-ui/Table";

import axios from "axios";
import { cyan600, blue800, red800 } from "material-ui/styles/colors";

const columns = [
    "Item",
    "Value"
];
const styles = {
    card: {
        marginTop: 30
    },
    div: {
        paddingTop: 5,
        paddingBottom:5,
        paddingLeft: 30,
        paddingRight:100
    },
    columns: {
       fields: {
            Item: {
                width: "40%",
                color: blue800
            },
            "Value": {
                width: "20%",
                color: red800
            }
       }
    }
};

class VehicleDetails extends React.Component {
    constructor(props) {
        super(props);
        this.state = this.getDefaultState();
    }

    getDefaultState() {
        return {
            details: []
        };
    }

    getDetails() {
        /*var reqObj = {
            method: "post",
            url: "/api/stats",
            headers:{
				"Content-Type": "application/json",
				Authorization: "Bearer " + localStorage.getItem("access_token")            
			}, 
            data: {
                startDate: this.props.filterObj.startDate,
                endDate: this.props.filterObj.endDate,
                vehicleList: this.props.filterObj.vehicleList
            }
        };
        axios(reqObj)
            .then(resp => {
                this.setState({ getGraphData: resp.data });
            })
            .catch(err => {
                this.setState(this.getDefaultState());
            });*/

        this.setState({
            details:[
                {Item:"Registration No", Value: "SBG1256"},
                {Item:"Average score", Value:56},
                {Item:"Average driving distance", Value: 200},
                {Item:"Total distance travelled on accident day", Value: 150},
                {Item:"Weather condition at the time of accident", Value: "Raining"},
                {Item:"Claim reference number", Value: "C120045"},
                {Item:"Claim amount", Value:10050},
                {Item:"Total accidents before", Value: 2},
                {Item:"Total claim amount so far", Value: 35000}
            ]
        });
    }

    componentDidMount() {
        this.getDetails();
    }

    componentWillReceiveProps(nextProps) {
        this.getDetails();
    }

    render() {
        return (
            <Card style={styles.card}>
                <CardHeader
                    title="Vehicle Details"
                    subtitle="Information about the vehicle"
                    actAsExpander={true}
                    showExpandableButton={true}
                />
                <CardText expandable={true}>
                    <div style={styles.div}>
                        <Table >
                            <TableBody displayRowCheckbox={false}>
                                {this.state.details.map((row, index) =>
                                    <TableRow key={index}>
                                        {columns.map(field =>
                                            <TableRowColumn
                                                style={styles.columns.fields[field]}
                                                key={field}
                                            >
                                                {row[field]}
                                            </TableRowColumn>
                                        )}
                                    </TableRow>
                                )}
                            </TableBody>
                        </Table>
                        </div>
                </CardText>
            </Card>
        );
    }
}

export default VehicleDetails;
