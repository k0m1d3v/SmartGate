import React from 'react';
import { View, Text, StyleSheet, Alert } from 'react-native';
import { Button, Title } from 'react-native-paper';
import ImagePicker from 'react-native-image-picker';




const Cars = () => {
  
  return (
    <View style={{ flex: 1, alignItems: 'center' }}>
      {/*qua ci sranno le auto presenti in garage*/}
      <Text style={style.button}>QUA VEDI LE AUTO PRESENTI NEL PARCHEGGIO NEL MOMENTO</Text>
    </View>
  );
};

const style = StyleSheet.create({
  button:{
    color:'red',
    fontSize: 18,
    bottom: -15,
    justifyContent: 'center',
    textAlign:"center"
  }
})
export default Cars;