import React from "react";
import PageBase from "../components/PageBase";
import Realtime from "../components/map/Realtime";
import Historical from "../components/map/Historical";
import { Tabs, Tab } from "material-ui/Tabs";
import FilterDrawer, { FilterObj } from "../components/filter/FilterDrawer";
import "leaflet/dist/leaflet.css";

const styles = {
    map: {
        height: "100%",
        width: "100%"
    }
};

class TrackingPage extends React.Component {
    constructor() {
        super();
        this.state = { filterObj: this.defaultFilter(1, 1) };
    }

    defaultFilter(startOffset, endOffset) {
        let start = new Date();
        start.setDate(start.getDate() - startOffset);

        let end = new Date();
        end.setDate(end.getDate() - endOffset);

        let filterObj = new FilterObj();
        filterObj.startDate = start;
        filterObj.endDate = end;
        filterObj.vehicleList = [];
        return filterObj;
    }

    applyFilter(filterObj) {
        this.setState({ filterObj: filterObj });
    }

    render() {
        return (
            <PageBase
                title="Tracking of Vehicles"
                navigation="Application / Tracking"
            >
                <div>
                    <Tabs>
                        <Tab label="Past Trip">
                            <div style={styles.map}>
                                <Historical filterObj={this.state.filterObj} />
                            </div>
                        </Tab>
                        <Tab label="Realtime">
                            <div style={styles.map}>
                                <Realtime filterObj={this.state.filterObj} />
                            </div>
                        </Tab>
                    </Tabs>
                    <FilterDrawer
                        filterObj={this.state.filterObj}
                        applyFilter={this.applyFilter.bind(this)}
                    />
                </div>

            </PageBase>
        );
    }
}

export default TrackingPage;
