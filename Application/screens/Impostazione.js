import React, { useState, useEffect, useRef } from "react";
import {
  View,
  StyleSheet,
  Modal,
  TextInput,
  Text,
  TouchableOpacity,
} from "react-native";
import { Button } from "react-native-paper";
import AsyncStorage from "@react-native-async-storage/async-storage";

const STORAGE_KEY = "@message_key";
let messaggioSalvato;

const Impostazione = () => {
  const [messaggio, setMessaggio] = useState("");
  const [isModalVisible, setModalVisible] = useState(false);
  const [tempMessaggio, setTempMessaggio] = useState("");
  const invia = () => {
    console.warn("Messaggio da inviare:", messaggio);
  };

  useEffect(() => {
    caricaMessaggio();
  }, []);

  const caricaMessaggio = async () => {
    try {
      messaggioSalvato = await AsyncStorage.getItem(STORAGE_KEY);
      if (messaggioSalvato !== null) {
        setMessaggio(messaggioSalvato);
      }
    } catch (error) {
      console.error("Errore nel caricamento del messaggio:", error);
    }
  };

  const salvaMessaggio = async (nuovoMessaggio) => {
    try {
      await AsyncStorage.setItem(STORAGE_KEY, nuovoMessaggio);
      setMessaggio(messaggioSalvato);
      alert("Messaggio salvato con successo!");
    } catch (error) {
      console.error("Errore nel salvataggio del messaggio:", error);
      alert("Non è stato possibile salvare il messaggio.");
    }
  };

  const buttonPressed = () => {
    setTempMessaggio(messaggio);
    setModalVisible(true);
  };

  const handleSave = () => {
    salvaMessaggio(tempMessaggio);
    messaggioSalvato = tempMessaggio;
    setModalVisible(false);
  };

  return (
    <View style={styles.container}>
      <Button onPress={buttonPressed} style={styles.button} mode="contained">
        Modifica Messaggio
      </Button>

      <Modal
        animationType="slide"
        transparent={true}
        visible={isModalVisible}
        onRequestClose={() => setModalVisible(false)}
      >
        <View style={styles.centeredView}>
          <View style={styles.modalView}>
            <Text style={styles.modalText}>Inserisci un messaggio</Text>
            <TextInput
              style={styles.input}
              onChangeText={setTempMessaggio}
              value={tempMessaggio}
              placeholder="Scrivi il tuo messaggio qui"
            />
            <View style={styles.buttonContainer}>
              <TouchableOpacity
                style={[styles.modalButton, styles.buttonCancel]}
                onPress={() => setModalVisible(false)}
              >
                <Text style={styles.textStyle}>Annulla</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={[styles.modalButton, styles.buttonSave]}
                onPress={handleSave}
              >
                <Text style={styles.textStyle}>Salva</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  button: {
    backgroundColor: "purple",
    padding: 10,
    borderRadius: 5,
  },
  centeredView: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "rgba(0, 0, 0, 0.5)",
  },
  modalView: {
    margin: 20,
    backgroundColor: "white",
    borderRadius: 20,
    padding: 35,
    alignItems: "center",
    shadowColor: "#000",
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 4,
    elevation: 5,
  },
  modalText: {
    marginBottom: 15,
    textAlign: "center",
    fontSize: 18,
  },
  input: {
    height: 40,
    width: 200,
    margin: 12,
    borderWidth: 1,
    padding: 10,
    borderRadius: 5,
  },
  buttonContainer: {
    flexDirection: "row",
    justifyContent: "space-between",
    width: "100%",
  },
  modalButton: {
    borderRadius: 5,
    padding: 10,
    elevation: 2,
    marginHorizontal: 10,
  },
  buttonCancel: {
    backgroundColor: "#2196F3",
  },
  buttonSave: {
    backgroundColor: "#4CAF50",
  },
  textStyle: {
    color: "white",
    fontWeight: "bold",
    textAlign: "center",
  },
});
export {messaggioSalvato};
export default Impostazione;