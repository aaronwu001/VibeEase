import React from "react";
import { View, Text, StyleSheet, TouchableOpacity } from "react-native";
import { Link } from "expo-router";
import { LinearGradient } from "expo-linear-gradient";
import { Button } from "react-native-paper";

export default function Index() {
  return (
    <LinearGradient
      colors={["#E6F7FF", "#D1EAF5", "#B9D9E8"]} // Soft, layered blues
      style={styles.container}
    >
      <View style={styles.contentContainer}>
        <Text style={styles.title}>VibeEase</Text>
        <Text style={styles.subtitle}>
          Connect with like-minded people effortlessly.
        </Text>
        <Link href="/select" style={styles.link}>
          <Button style={styles.button} labelStyle={styles.buttonLabel}>
            Find Your Vibe
          </Button>
        </Link>
      </View>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  contentContainer: {
    alignItems: "center",
    paddingHorizontal: 30,
  },
  title: {
    fontSize: 42,
    fontWeight: "800",
    color: "#333",
    marginBottom: 10,
    textAlign: "center",
    fontFamily: "System",
    letterSpacing: 1,
  },
  subtitle: {
    fontSize: 18,
    color: "#555",
    marginBottom: 30,
    textAlign: "center",
    fontFamily: "System",
    lineHeight: 26,
  },
  link: {
    marginTop: 20,
    width: "100%",
  },
  button: {
    backgroundColor: "#3498db",
    paddingVertical: 10, // Increased padding for more height
    paddingHorizontal: 20, // Increased horizontal padding for a wider button
    borderRadius: 20, // Rounded corners for a more modern look
    alignItems: "center",
    justifyContent: "center",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 6,
    elevation: 3,
  },
  buttonLabel: {
    fontSize: 20, // Larger font size for the button text
    fontWeight: "600",
    color: "#fff", // White text color
    textAlign: "center",
  },
});
