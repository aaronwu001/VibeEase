// app/other.tsx
import React from "react";
import { View, Text, Button, StyleSheet } from "react-native";
import { Link } from "expo-router"; // Import Link from expo-router

export default function Index() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>This is the Other Page!</Text>
      <Link href="/record">{"go to record"}</Link>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  title: {
    fontSize: 24,
    marginBottom: 20,
  },
});
