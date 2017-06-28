import React, {PropTypes} from 'react';
import OverviewMap from './OverviewMap';
import {Card, CardHeader, CardText} from 'material-ui/Card';

const styles = {
    card: {
        marginTop: 30
    }
}

class GeoVisualization extends React.Component {
    render(){
        return (
            <Card style={styles.card}>
                <CardHeader
                    title="Geo Visualization"
                    subtitle="Geo Statistics Visualization"
                    actAsExpander={true}
                    showExpandableButton={true}
                />
                <CardText expandable={true}>
                    <OverviewMap filterObj = {this.props.filterObj}/>
                </CardText>
            </Card>
        );
    }
}

export default GeoVisualization;