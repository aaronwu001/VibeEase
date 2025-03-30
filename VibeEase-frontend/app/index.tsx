import React from "react";
import { View, Text, StyleSheet, TouchableOpacity } from "react-native";
import { Link } from "expo-router";
import { LinearGradient } from "expo-linear-gradient";

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
          <TouchableOpacity style={styles.button}>
            <Text style={styles.buttonText}>Find Your Vibe</Text>
          </TouchableOpacity>
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
    paddingVertical: 16,
    paddingHorizontal: 40,
    borderRadius: 8,
    alignItems: "center",
    justifyContent: "center",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 6,
    elevation: 3,
  },
  buttonText: {
    color: "#fff",
    fontSize: 20,
    fontWeight: "600",
    fontFamily: "System",
  },
});
