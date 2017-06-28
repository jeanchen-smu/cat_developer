import React, {PropTypes} from "react";
import {
    Card,
    CardActions,
    CardHeader,
    CardText,
    Tabs,
    Tab
} from "material-ui/Tabs";
import SwipeableViews from "react-swipeable-views";
import FMBarChart from "./charts/FMBarChart";
import FMLineChart from "./charts/FMLineChart";
import {
    cyan600,
    pink600,
    purple600,
    orange600,
    red600,
    blue600,
    yellow900
} from "material-ui/styles/colors";

const styles = {
    slide: {
        padding: 10
    }
};

class StatGraphs extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            slideIndex: 0
        };
    }

    handleChange = value => {
        this.setState({
            slideIndex: value
        });
    };

    render() {
        return (
            <div>
                <Tabs
                    onChange={this.handleChange}
                    value={this.state.slideIndex}
                >
                    <Tab label="Score Distribution" value={0} />
                    <Tab label="Average Score" value={1} />
                    <Tab label="Average Distance" value={2} />
                </Tabs>
                <SwipeableViews
                    index={this.state.slideIndex}
                    onChangeIndex={this.handleChange}
                >
                    <div style={styles.slide}>
                        <FMBarChart
                            headerColor={orange600}
                            title="Vehicle Score Distribution"
                            data={this.props.data.scoreDistribution}
                            color={blue600}
                        />
                    </div>
                    <div style={styles.slide}>
                        <FMLineChart
                            headerColor={pink600}
                            title="Average Driving Score"
                            data={this.props.data.averageScore}
                            color={purple600}
                        />
                    </div>
                    <div style={styles.slide}>
                        <FMLineChart
                            headerColor={red600}
                            title="Average Driving Distance"
                            data={this.props.data.averageDistance}
                            color={yellow900}
                        />
                    </div>
                </SwipeableViews>
            </div>
        );
    }
}

StatGraphs.propTypes = {
    data: PropTypes.object
}

export default StatGraphs