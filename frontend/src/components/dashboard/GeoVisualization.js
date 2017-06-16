import React, {PropTypes} from 'react';
import OverviewMap from './OverviewMap';
import {Card, CardHeader, CardText} from 'material-ui/Card';

class GeoVisualization extends React.Component {
    render(){
        return (
            <Card initiallyExpanded={true}>
                <CardHeader
                    title="Geo Visualiztion"
                    subtitle="Geo Statistics Visualization"
                    actAsExpander={true}
                    showExpandableButton={true}
                />
                <CardText expandable={true}>
                    <OverviewMap />
                </CardText>
            </Card>
        );
    }
}

export default GeoVisualization;