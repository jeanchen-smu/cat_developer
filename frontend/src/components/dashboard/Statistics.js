import React from 'react';
import {Card, CardHeader, CardText} from 'material-ui/Card';
import StatGraphs from './StatGraphs';

class Statistics extends React.Component {

  render() {
    return (
        <Card>
            <CardHeader
                title="Statistics"
                subtitle="Statistics Graphs"
                actAsExpander={true}
                showExpandableButton={true}
            />
            <CardText expandable={true}>
                <StatGraphs />
            </CardText>
        </Card>
    );
  }
}

export default Statistics;
