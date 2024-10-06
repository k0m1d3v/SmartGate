import * as React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { Provider as PaperProvider } from 'react-native-paper';
import Dashboard from './screens/Dashboard';
import VoltieTarghe from './screens/Volti e Targhe';
import * as SplashScreen from 'expo-splash-screen';
import cars from './screens/Cars';
import Impostazione from './screens/Impostazione';


const Stack = createNativeStackNavigator();

// Prevent the splash screen from hiding automatically
SplashScreen.preventAutoHideAsync();

export default function App() {
  React.useEffect(() => {
    // Simulate some loading tasks
    const prepare = async () => {
      // You can add any initialization tasks here
      await new Promise(resolve => setTimeout(resolve, 2000)); // Simulate a 2-second loading task
      await SplashScreen.hideAsync();
    };

    prepare();
  }, []);

  return (
    <PaperProvider>
      <NavigationContainer>
        <Stack.Navigator initialRouteName="SmartGate">
          <Stack.Screen name="SmartGate" component={Dashboard} />
          <Stack.Screen name="Volti e Targhe" component={VoltieTarghe} />
          <Stack.Screen name="Cars" component={cars} />
          <Stack.Screen name="Impostazione" component={Impostazione} />
        </Stack.Navigator>
      </NavigationContainer>
    </PaperProvider>
  );
}
