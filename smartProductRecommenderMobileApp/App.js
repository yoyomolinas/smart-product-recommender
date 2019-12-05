import React, {useEffect, useState} from 'react';
import {StyleSheet, View} from 'react-native';
import Header from './components/Header';
import MainPage from './screens/MainPage';
import ProductShot from './screens/ProductShot';
import ImgPicker from './screens/ImgPicker';
import RecommendationScreen from "./screens/RecommendationScreen";
import Loading from "./screens/Loading";

export default function App() {
    const [userName, setUserName] = useState();
    const [cameraMode, setCameraMode] = useState();
    const [imageData, setImageData] = useState();
    const [max_price, setMax] = useState();
    const [min_price, setMin] = useState();
    const [showReco, setReco] = useState();
    const [isStarted, setStarted] = useState();
    const [matching_data,setData] = useState([]);
    const [uniqueId,setId] = useState();
    const [imageSent,setSend] = useState();

    // async function componentDidMount(){
    //     let result =await fetch('http://35.223.191.99:5000/matching_products')
    //         .then((response) => response.json())
    //         .then((responseJson) => {
    //                  setData(responseJson);
    //
    //         });
    //     return result;
    // }

    // async function postSavedImage(){
    //     const d = new Date();
    //     const id = d.getTime();
    //     setId(id);
    //     let result =await fetch('http://35.223.191.99:5000/add_product',{
    //             method: 'POST',
    //             body : {"id": id , "image":imageData, "minPrice":min_price, "maxPrice":max_price}
    //         }).then ( () => {
    //             console.log("success");
    //             setSend(true);
    //         }, error => {
    //             console.log("getting error");
    //             console.log(error);
    //         }
    //         );
    //      return result;
    //
    // }

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

    let content = <Loading output={"Application Loading"}/>;
    setTimeout(() => {
        setStarted(true);

    }, 3000);
    
    if (isStarted) {
        content = <MainPage onMainPageLoad={mainPageHandler}/>;
    }

    if (userName) {
        content = <ProductShot nameOfUser={userName} onCameraPageClick={cameraHandler}/>;
    }

    if (cameraMode) {
        content = <ImgPicker onSetMax={maxPriceHandler} onSetMin={minPriceHandler}
                             onImageData={imageDataHandler}/>;
    }

    if (max_price && min_price && imageData && !imageSent) {
        content = <Loading output={"Getting Best Matches"}/>;
        // postSavedImage();
        setTimeout(() => {
            // componentDidMount();
            setReco(true);
        }, 5000);


    }
// && matching_data TODO: LATER ADD THE LEFT EXPRESSION SO THAT IT WON'T REDİRECT TO RECOMMENDATION PAGE WITHOUT FETCHED DATA
    if (showReco) {//change useDemo to false when everything is set!!
        content = <RecommendationScreen imageData={matching_data} productId={uniqueId} useDemo={true}/>;
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