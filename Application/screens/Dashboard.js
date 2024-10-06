import React, { useEffect } from 'react';
import { View, StyleSheet, ScrollView, TouchableOpacity, Text, Image} from 'react-native';
import { Card, Title, Paragraph } from 'react-native-paper';
import { requestPermissions, sendNotification } from '../notificationHelper'; // Import the helper functions
import {messaggioSalvato} from './Impostazione';



function invia() {
  sendNotification("Messaggio", messaggioSalvato);
}

//let Messaggio= prompt('Inserire Messaggio: ');



const Dashboard = ({ navigation }) => {
  useEffect(() => {
    requestPermissions(); // Request notification permissions on component mount
  }, []);

  const handleCardPress = (screenName) => {
    navigation.navigate(screenName);
  };

  return (
    <ScrollView style={styles.container}>
      <View>
        <Image style={styles.image} source={require('../Images/SmartGate Icon.png')}></Image>
      </View>
      <View style={styles.row}>
        <TouchableOpacity style={styles.cell} onPress={() => handleCardPress('Volti e Targhe')}>
          <Card style={styles.card}>
            <Card.Content>
              <Title>Volti e Targhe</Title>
              <Paragraph>Gestisci Caricamenti</Paragraph>
            </Card.Content>
          </Card>
        </TouchableOpacity>
      </View>

      <View style={styles.row}>
        <TouchableOpacity style={styles.cell} onPress={invia}>
          <Card style={styles.card}>
            <Card.Content>
              <Title>Messaggio</Title>
              <Paragraph>Invia messaggio</Paragraph>
            </Card.Content>
          </Card>
        </TouchableOpacity>
        <TouchableOpacity style={styles.cell} onPress={() => handleCardPress('Cars')}>
          <Card style={styles.card}>
            <Card.Content>
              <Title>Cars</Title>
              <Paragraph>Cars in garage</Paragraph>
            </Card.Content>
          </Card>
        </TouchableOpacity>
      </View>

      <View style={styles.row}>
        <TouchableOpacity style={styles.cell} onPress={() => handleCardPress('Impostazione')}>
          <Card style={styles.card}>
            <Card.Content>
              <Title>Impostazione</Title>
              <Paragraph>Gestisci Impostazioni</Paragraph>
            </Card.Content>
          </Card>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 10,
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 20,
  },
  cell: {
    flex: 1,
    marginHorizontal: 5,
  },
  image: {
    width: 300,
    height: 180,
    borderWidth: 5,
    borderRadius: 20,
    left: 20,
    marginBottom: 30,
  },
  card: {
    height: 90,
  }
});
export default Dashboard;
