import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, Alert, Image, TouchableOpacity, TextInput, Platform } from 'react-native';
import { Button, Menu, Provider } from 'react-native-paper';
import * as ImagePicker from 'expo-image-picker';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';

const Targhe = () => {
  const [image, setImage] = useState(null);
  const [visible, setVisible] = useState(false);
  const [licensePlate, setLicensePlate] = useState('');

  // Richiedi i permessi al caricamento del componente
  useEffect(() => {
    (async () => {
      if (Platform.OS === 'android') {
        const { status: cameraStatus } = await ImagePicker.requestCameraPermissionsAsync();
        const { status: libraryStatus } = await ImagePicker.requestMediaLibraryPermissionsAsync();
        
        if (cameraStatus !== 'granted' || libraryStatus !== 'granted') {
          Alert.alert('Devi abilitare i permessi di fotocamera e libreria multimediale per utilizzare l\'app!');
        }
      }
    })();
  }, []);

  // Funzione per aprire il menu
  const openMenu = () => setVisible(true);

  // Funzione per chiudere il menu
  const closeMenu = () => setVisible(false);

  // Funzione per selezionare un'immagine dalla galleria
  const pickImage = async () => {
    closeMenu();

    const permissionResult = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (!permissionResult.granted) {
      Alert.alert('Permesso per accedere alla libreria multimediale richiesto!');
      return;
    }

    const pickerResult = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      quality: 1,
    });

    if (!pickerResult.canceled) {
      setImage(pickerResult.assets[0].uri);
    }
  };

  // Funzione per scattare una foto
  const takePhoto = async () => {
    closeMenu();

    const permissionResult = await ImagePicker.requestCameraPermissionsAsync();
    if (!permissionResult.granted) {
      Alert.alert('Permesso per accedere alla fotocamera richiesto!');
      return;
    }

    const pickerResult = await ImagePicker.launchCameraAsync({
      allowsEditing: true,
      quality: 1,
    });

    if (!pickerResult.canceled) {
      setImage(pickerResult.assets[0].uri);
    }
  };

  // Funzione per caricare la foto
  const uploadFace = async () => {
    if (!image) {
      Alert.alert('Nessuna immagine selezionata!');
      return;
    }

    const formData = new FormData();
    formData.append('image', {
      uri: image,
      name: 'face.jpg',
      type: 'image/jpeg',
    });

    try {
      const response = await fetch('http://172.18.3.80:5000/upload_face', {
        method: 'POST',
        body: formData,
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const data = await response.json();
      if (response.ok) {
        Alert.alert(data.message);
        setImage(null);
      } else {
        Alert.alert('Errore durante l\'upload della foto');
      }
    } catch (error) {
      console.error('Errore durante l\'upload:', error);
      Alert.alert('Errore nel caricamento della foto.');
    }
  };

  // Funzione per aggiungere una targa
  const addPlate = async () => {
    if (!licensePlate) {
      Alert.alert('Inserisci una targa!');
      return;
    }

    try {
      const response = await fetch('http://172.18.3.80:5000/add_plate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ plate: licensePlate }),
      });

      const data = await response.json();
      if (response.ok) {
        Alert.alert(data.message);
        setLicensePlate('');
      } else {
        Alert.alert(data.error);
      }
    } catch (error) {
      console.error('Errore durante l\'aggiunta della targa:', error);
      Alert.alert('Errore nell\'aggiunta della targa.');
    }
  };

  return (
    <Provider>
      <View style={styles.container}>
        <Text style={styles.title}>Volti e Targhe</Text>
        <Menu
          visible={visible}
          onDismiss={closeMenu}
          anchor={
            <TouchableOpacity onPress={openMenu}>
              <LinearGradient colors={['#ff1b6b', '#45caff']} style={styles.iconButton}>
                <Ionicons name="add" size={30} color="white" />
              </LinearGradient>
            </TouchableOpacity>
          }
          style={styles.menu}
        >
          <Menu.Item
            onPress={pickImage}
            title="Seleziona Foto"
            leadingIcon={() => <Ionicons name="images-outline" size={24} color="black" />}
          />
          <Menu.Item
            onPress={takePhoto}
            title="Scatta Foto"
            leadingIcon={() => <Ionicons name="camera-outline" size={24} color="black" />}
          />
        </Menu>

        {image && (
          <View>
            <Image source={{ uri: image }} style={styles.image} />
            <Button onPress={uploadFace}>Carica Foto</Button>
          </View>
        )}

        <TextInput
          value={licensePlate}
          onChangeText={setLicensePlate}
          placeholder="Inserisci Targa"
          style={styles.input}
        />
        <Button onPress={addPlate}>Aggiungi Targa</Button>
      </View>
    </Provider>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 16,
  },
  title: {
    fontSize: 24,
    marginBottom: 20,
  },
  menu: {
    marginBottom: 20,
  },
  iconButton: {
    padding: 10,
    borderRadius: 50,
    alignItems: 'center',
  },
  image: {
    width: 200,
    height: 200,
    marginTop: 10,
    borderRadius: 10,
  },
  input: {
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    marginTop: 20,
    paddingHorizontal: 10,
    width: '80%',
    borderRadius: 5,
  },
});

export default Targhe;
