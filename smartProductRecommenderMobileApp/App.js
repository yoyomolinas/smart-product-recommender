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
    const [max_price, setMax] = useState();
    const [min_price, setMin] = useState();
    const [showReco, setReco] = useState(0);
    const [isStarted, setStarted] = useState();
    const [matching_data,setData] = useState([]);
    const [uniqueId,setId] = useState();
    const [imageSent,setSend] = useState();

    async function componentDidMount(){
        let result =await fetch('http://35.223.191.99:5000/products')
            .then((response) => response.json())
            .then((responseJson) => {
                     setData(responseJson);
    
            });
        return result;
    }

    async function postSavedImage(image_data,minPrice,maxPrice){
        const min = minPrice;
        const max = maxPrice;
        const image = image_data;
        const d = new Date();
        const id = d.getTime();
        setId(id);
        let result =await fetch('http://35.223.191.99:5000/add_product',{
                method: 'POST',
                headers: {
                    Accept: 'application/json',
                     'Content-Type': 'application/json',
                         },
                body : JSON.stringify({"id": id , "image":image, "minPrice":min, "maxPrice":max
            }),
        }).then(success => {
            console.log("Success");
            setSend(true);
          }, error => {
            console.log(error);
          });
         return result;    
    }

    const mainPageHandler = selectedName => {
        setUserName(selectedName);
    };
    const newSearchHandler = () => {
        setReco(false);
        setMin(null);
        setMax(null);
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
    const imageTransactionHandler = () => {
        setTimeout(() => {
            componentDidMount();
        }, 4000);        
    };
    const showImagePicker = () => {
        content = <ImgPicker onSetMax={maxPriceHandler} onSetMin={minPriceHandler} onImageData={imageDataHandler} onTransaction={imageTransactionHandler}/>;
    };
    const showRecoScreen = () => {
        content = <Loading output={"Getting Best Matches"}/>;
        setTimeout(() => {
            setReco(true);
        }, 5000);

    };
    const imageDataHandler = (imageData,minPrice,maxPrice) => {
        postSavedImage(imageData,minPrice,maxPrice);
        setTimeout(() => {
            imageTransactionHandler();
        }, 1000);
    };

    setTimeout(() => {
        setStarted(true);
    }, 3000);
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

    if (max_price && min_price && !imageSent) {
       showRecoScreen();
    }
    if (showReco ) {
        content = <RecommendationScreen productData={matching_data} productId={uniqueId} useDemo={true}/>;
        return (
            <View style={styles.screen}>
                <Header />
                {content}
                <NewSearch onNewSearch={newSearchHandler} />
            </View>
        );
    }else{
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