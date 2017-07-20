import React from "react";
import { Route, IndexRoute } from "react-router";
import App from "./containers/App";
import NotFoundPage from "./containers/NotFoundPage.js";
import LoginPage from "./containers/LoginPage";
import Dashboard from "./containers/DashboardPage";
import RankPage from "./containers/RankPage";
import TrackingPage from "./containers/TrackingPage";
//import AccidentPage from "./containers/AccidentPage";
import OfferPage from "./containers/OfferPage";
import AccidentAnalysis from "./containers/AccidentAnalysis";

function loggedIn() {
    return localStorage.getItem("access_token") != null;
}

function requireAuth(nextState, replace) {
    if (!loggedIn()) {
        replace({
            pathname: "/login"
        });
    }
}

export default (
    <Route>
        <Route path="/" component={LoginPage} />
        <Route path="/login" component={LoginPage} />
        <Route path="/home" component={App} onEnter={requireAuth}>
            <IndexRoute component={Dashboard} />
            <Route path="dashboard" component={Dashboard} />
            <Route path="tracking" component={TrackingPage} />
            <Route path="rank" component={RankPage} />
            {/*<Route path="accident" component={AccidentPage} />*/}
            <Route path="offer" component={OfferPage} />
            <Route path="accidentanalysis" component={AccidentAnalysis} />
            <Route path="*" component={NotFoundPage} />
        </Route>
    </Route>
);
