import React, { PropTypes } from "react";
import OverviewMap from "./OverviewMap";
import { Card, CardHeader, CardText } from "material-ui/Card";

const styles = {
    card: {
        marginTop: 30
    }
};

class GeoVisualization extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            mapData: [] //array of [Lat, Long, Speed...]
        };
    }
    getMapData() {
        var reqObj = {
            method: "post",
            url: "/api/overview",
            headers: {
                "Content-Type": "application/json"
            },
            data: {
                startDate: this.props.filterObj.startDate,
                endDate: this.props.filterObj.endDate,
                vehicleList: this.props.filterObj.vehicleList
            }
        };
        axios(reqObj)
            .then(resp => {
                this.setState({ mapData: resp.data });
            })
            .catch(err => {
                this.setState({ mapData: [] });
            });
    }

    componentWillMount() {
        this.getMapData();
    }

    render() {
        return (
            <Card style={styles.card}>
                <CardHeader
                    title="Geo Visualization"
                    subtitle="Heat Map of Trips"
                    actAsExpander={true}
                    showExpandableButton={true}
                />
                <CardText expandable={true}>
                    <OverviewMap
                        filterObj={this.props.filterObj}
                        data={this.state.mapData}
                    />
                </CardText>
            </Card>
        );
    }
}

export default GeoVisualization;
