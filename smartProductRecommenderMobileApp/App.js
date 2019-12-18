import React, {useEffect, useState} from 'react';
import {StyleSheet, View} from 'react-native';
import Header from './components/Header';
import MainPage from './screens/MainPage';
import ProductShot from './screens/ProductShot';
import ImgPicker from './screens/ImgPicker';
import RecommendationScreen from "./screens/RecommendationScreen";
import Loading from "./screens/Loading";
import NewSearch from './components/NewSearch';

export default function App() {
    const [userName, setUserName] = useState();
    const [cameraMode, setCameraMode] = useState();
    const [showReco, setReco] = useState(false);
    const [isStarted, setStarted] = useState();
    const [isLoading, setLoading] = useState();
    const [matching_data, setData] = useState([]);



     function componentDidMount(uniqId) {

        let result =  fetch('http://35.223.191.99:5000/get_matches?id='+uniqId)
            .then((response) => response.json())
            .then((responseJson) => {
                setData(responseJson);
                console.log(responseJson);
            });
        return result;
    }

     function postSavedImage(image_data, minPrice, maxPrice) {
        const min = minPrice;
        const max = maxPrice;
        const image = image_data;
        const d = new Date();
        const id = d.getTime();

        let result =  fetch('http://35.223.191.99:5000/add_product', {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "id": id, "image": image, "minPrice": min, "maxPrice": max
            }),
        });
        return id;
    }

    const mainPageHandler = selectedName => {
        setUserName(selectedName);
    };
    const newSearchHandler = () => {
        setReco(false);
        showImagePicker();
    };

    const cameraHandler = cameraMode => {
        setCameraMode(cameraMode);
    };

    const imageTransactionHandler = (id) => {
      setTimeout(() => {
      componentDidMount(id);
    }, 4000);

    };
    const showImagePicker = () => {
        content = <ImgPicker onImageData={imageDataHandler} />;
    };
    const showRecoScreen = () => {
        content = <RecommendationScreen productData={matching_data} useDemo={false}/>;
    };
    const imageDataHandler = (imageData, minPrice, maxPrice) => {
      let uniqueId;
         setLoading(true);
         uniqueId = postSavedImage(imageData,minPrice,maxPrice);
        imageTransactionHandler(uniqueId);
        setTimeout(() => {
            setLoading(false);
            setReco(true);
        }, 7100);
    };

    setTimeout(() => {
        setStarted(true);
    }, 2000);

    let content = <Loading output={"Application Loading"}/>;
    if (isStarted) {
        content = <MainPage onMainPageLoad={mainPageHandler}/>;
    }

    if (userName) {
        content = <ProductShot nameOfUser={userName} onCameraPageClick={cameraHandler}/>;
    }
    if (cameraMode) {
        showImagePicker();
    }
    if (isLoading) {
        content = <Loading output={"Getting Best Matches"}/>;
    }

    if (showReco) {
        showRecoScreen();
        return (
            <View style={styles.screen}>
                <Header/>
                {content}
                <NewSearch onNewSearch={newSearchHandler}/>
            </View>
        );
    } else {
        return (
            <View style={styles.screen}>
                <Header/>
                {content}
            </View>
        );

    }
}


const styles = StyleSheet.create({
    screen: {
        flex: 1
    }
});
