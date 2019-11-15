import React, {useState,Component} from 'react';
import {StyleSheet, View} from 'react-native';
import * as Filesystem from 'expo-file-system';
import Header from './components/Header';
import MainPage from './screens/MainPage';
import ProductShot from './screens/ProductShot';
import ImgPicker from './screens/ImgPicker';



export default function App() {
    const [userName, setUserName] = useState();
    const [cameraMode, setCameraMode] = useState();
    const [takenImage, setImage] = useState();
    const [max_price, setMax] = useState();
    const [min_price, setMin] = useState();

    const saveImage = () => {
      return async dispatch => {
        const imageName = takenImage.split('/').pop();
        const pathName = Filesystem.documentDirectory + imageName;
        console.log(imageName);
        try {
          await Filesystem.moveAsync({
            from: takenImage,
            to: pathName
          });
        } catch (err) {
          console.log(err);
          throw(err);
        }
        dispatch({type : 'ADD_PLACE',placeData: {imageName : pathName}})
        console.log("Succeeded");
      };
    };

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

    const imageTakenHandler = (pickedImage) => {
        setImage(pickedImage);
    };

    let content = <MainPage onMainPageLoad={mainPageHandler}/>;

    if (userName) {
        content = <ProductShot nameOfUser={userName} onCameraPageClick={cameraHandler}/>;
    }

    if (cameraMode) {
        content = <ImgPicker onImagePicked={imageTakenHandler} onSetMax={maxPriceHandler} onSetMin={minPriceHandler}/>
    }

    if(max_price && min_price && takenImage){
      saveImage();
      console.log(takenImage);
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
