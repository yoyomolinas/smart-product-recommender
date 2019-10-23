import React, {useState} from 'react';
import { StyleSheet, Text, View,Button } from 'react-native';

export default function App() {
  const [outputText , setOutputText] = useState('Welcome to Smart Product Recommender')
  return (
    <View style={styles.container}>
      <Text>{outputText}</Text>
      <Button title= "Go To Product Page" onPress={() => setOutputText('Product page')} />
      <Text>Find your best match!</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
