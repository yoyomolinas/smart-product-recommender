import React, {useEffect,useState} from 'react';
import {StyleSheet, View} from 'react-native';
import Header from './components/Header';
import MainPage from './screens/MainPage';
import ProductShot from './screens/ProductShot';
import ImgPicker from './screens/ImgPicker';
import customData from './db.json';
import FileSystem from 'react-native-filesystem';
import {write} from "react-native-fs";

export default function App() {
    const [userName, setUserName] = useState();
    const [cameraMode, setCameraMode] = useState();
    const [imageData, setImageData] = useState();
    const [max_price, setMax] = useState();
    const [min_price, setMin] = useState();

    // useEffect(()=>{
    //
    // });

    const mainPageHandler = selectedName => {
        setUserName(selectedName);
    };

    const cameraHandler = cameraMode => {
        setCameraMode(cameraMode);
    };
    const maxPriceHandler = maxPrice => {
        setMax(maxPrice);
    };
    const minPriceHandler = minPrice => {
        setMin(minPrice);
    };
    const imageDataHandler = imageData => {
        setImageData(imageData);
    };


    let content = <MainPage onMainPageLoad={mainPageHandler}/>;

    if (userName) {
        content = <ProductShot nameOfUser={userName} onCameraPageClick={cameraHandler}/>;
    }

    if (cameraMode) {
        content = <ImgPicker onSetMax={maxPriceHandler} onSetMin={minPriceHandler}
                             onImageData={imageDataHandler}/>
    }

    if (max_price && min_price && imageData) {
        console.log(imageData.substring(0, 10));

    }

    return (
        <View style={styles.screen}>
            <Header title="Koc University"/>
            {content}
        </View>
    );
}

const styles = StyleSheet.create({
    screen: {
        flex: 1
    }
});
