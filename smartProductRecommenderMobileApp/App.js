import React, { useState } from 'react';
import { StyleSheet, View } from 'react-native';

import Header from './components/Header';
import MainPage from './screens/MainPage';
import ProductShot from './screens/ProductShot';

export default function App() {
  const [userName,setUserName] = useState();

  const mainPageHandler = selectedName => {
    setUserName(selectedName);
  };

  let content = <MainPage onMainPageLoad={mainPageHandler} />;

  if (userName) {
    content = <ProductShot nameOfUser={userName} />;
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
