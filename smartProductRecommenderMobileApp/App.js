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
    userName = null;

    componentDidMount() {
        return fetch('products')
            .then((response) => response.json())
            .then((responseJson) => {
                this.setState({
                    isLoading: false,
                    dataSource: responseJson
                })
            })
    }


    // const [userName, setUserName] = useState();
    // const [cameraMode, setCameraMode] = useState();
    // const [imageData, setImageData] = useState();
    // const [max_price, setMax] = useState();
    // const [min_price, setMin] = useState();
    //
     mainPageHandler = selectedName => {
        this.userName = selectedName;
    };
    //
    //  cameraHandler = cameraMode => {
    //     setCameraMode(cameraMode);
    // };
    //  maxPriceHandler = maxPrice => {
    //     setMax(maxPrice);
    // };
    //  minPriceHandler = minPrice => {
    //     setMin(minPrice);
    // };
    //  imageDataHandler = imageData => {
    //     setImageData(imageData);
    // };
    content = <MainPage onMainPageLoad={this.mainPageHandler}/>;

    // if (userName) {
    //     content = <ProductShot nameOfUser={userName} onCameraPageClick={cameraHandler}/>;
    // }
    //
    // if (cameraMode) {
    //     content = <ImgPicker onSetMax={maxPriceHandler} onSetMin={minPriceHandler}
    //                          onImageData={imageDataHandler}/>
    // }
    //
    // if (max_price && min_price && imageData) {
    //     console.log(imageData.substring(0, 10));
    // }


//productData={this.state.product_data}
//     content = <RecommendationScreen/>;

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

