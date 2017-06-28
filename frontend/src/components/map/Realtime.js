import React, { PropTypes } from "react";
import LocationMap from "./LocationMap";
import axios from "axios";
import "leaflet/dist/leaflet.css";
//import Data from "../../data";

class Realtime extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            mapData: []
        };
    }

    componentWillMount() {
        this.updateData();
    }

    componentDidMount() {
        this.timerID = setInterval(this.updateData.bind(this), 60 * 1000);
    }

    componentWillUnmount() {
        clearInterval(this.timerID);
    }

    updateData() {
        var reqObj = {
            method: "post",
            url: "/api/realtime",
            headers: {
                "Content-Type": "application/json"
            },
            data: {
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

    render() {
        return (
            <div>
                <LocationMap data={this.state.mapData} />
            </div>
        );
    }
}

Realtime.propTypes = {
    vehicleList: PropTypes.array
};

export default Realtime;
