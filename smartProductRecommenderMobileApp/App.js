import React, { useState } from 'react';
import { StyleSheet, View } from 'react-native';

import Header from './components/Header';
import MainPage from './screens/MainPage';
import ProductShot from './screens/ProductShot';
import ImgPicker from './screens/ImgPicker';

export default function App() {
  const [userName,setUserName] = useState();
  const [cameraMode,setCameraMode] = useState();
  const [takenImage, setTakenImage] = useState();

  const mainPageHandler = selectedName => {
    setUserName(selectedName);
  };

  const cameraHandler = cameraMode => {
    setCameraMode(cameraMode);
  }

  const imageTakenHandler = pickedImage => {
    setTakenImage(pickedImage);
  }

  let content = <MainPage onMainPageLoad={mainPageHandler} />;

  if (userName) {
    content = <ProductShot nameOfUser={userName} onCameraPageClick={cameraHandler}/>;
  }

  if (cameraMode) {
    content = <ImgPicker onImagePicked={imageTakenHandler}/>
  }

  return (
    <View style={styles.screen}>
      <Header title="Koc University" />
      {content}
    </View>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1
  }
});
