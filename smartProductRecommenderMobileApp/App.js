import React, {Component, useEffect, useState} from 'react';
import {StyleSheet, View} from 'react-native';
import RecommendationScreen from './screens/RecommendationScreen';
import Header from './components/Header';
import MainPage from './screens/MainPage';
import ProductShot from './screens/ProductShot';
import ImgPicker from './screens/ImgPicker';
import Text from "react-native-web/dist/exports/Text";

const  styles = StyleSheet.create({
    screen: {
        flex: 1
    }
});

export default class App extends Component {

    constructor(props) {
        super(props);
        this.state = {
            isLoading: true,
            dataSource: []
        }
    }

    mainPageHandler = selectedName => {
        this.userName = selectedName;
        this.decidePageNavigation();
    };
    cameraHandler = cameraMode => {
        this.cameraMode = cameraMode;
        this.decidePageNavigation();
    };
    maxPriceHandler = maxPrice => {
        this.max_price = maxPrice;
        this.decidePageNavigation();
    };
    minPriceHandler = minPrice => {
        this.min_price = minPrice;
        this.decidePageNavigation();
    };
    imageDataHandler = imageData => {
        this.imageData = imageData;
        this.decidePageNavigation();
    };

    componentDidMount() {
        return fetch('http://0.0.0.0:5000/products')
            .then((response) => response.json())
            .then((responseJson) => {
                this.setState({
                    isLoading: false,
                    dataSource: responseJson
                })
            })
    }

    userName = null;
    cameraMode = null;
    imageData = null;
    max_price = null;
    min_price = null;

    content = <MainPage onMainPageLoad={this.mainPageHandler}/>;

    decidePageNavigation = () => {
        if (this.userName) {
            this.content = <ProductShot nameOfUser={this.userName} onCameraPageClick={this.cameraHandler}/>;
        }

        if (this.cameraMode) {
            this.content = <ImgPicker onSetMax={this.maxPriceHandler} onSetMin={this.minPriceHandler}
                                      onImageData={this.imageDataHandler}/>
        }

        if (this.max_price && this.min_price && this.imageData) {
            console.log(this.imageData.substring(0, 10));
            this.content = <RecommendationScreen/>;
        }
    };



    render() {
        // if (this.state.dataSource.length > 0){
        //     console.log(this.state.dataSource);

        return (
            <View style={styles.screen}>
                <Header title="Koc University"/>
                {this.content}
            </View>
        );


    }



}

