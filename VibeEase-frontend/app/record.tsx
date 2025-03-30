import React, { useState } from "react";
import { View, Text, Alert, StyleSheet } from "react-native";
import { Audio } from "expo-av";
import * as FileSystem from "expo-file-system";
import * as Sharing from "expo-sharing";
import { Button } from "react-native-paper";
import { Link } from "expo-router"; // Import Link from expo-router

export default function Record() {
  const [hasPermission, setHasPermission] = useState(false);
  const [recording, setRecording] = useState<Audio.Recording | null>(null);
  const [isRecording, setIsRecording] = useState(false);
  const [audioUri, setAudioUri] = useState<string | null>(null);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const userId1 = "67e8259487c915a2c5841751";
  const userId2 = "67e82599a7a20b37bda740fd";

  const requestPermissions = async () => {
    // Check if the app already has permissions
    const { status } = await Audio.requestPermissionsAsync();

    if (status === "granted") {
      setHasPermission(true);
    } else {
      setHasPermission(false);
      Alert.alert("Permission Denied", "Enable microphone access to record.");
    }
  };

  const startRecording = async () => {
    try {
      if (isRecording) {
        console.log("Recording already in progress.");
        return; // Prevent starting a new recording if one is active
      }

      if (!hasPermission) {
        await requestPermissions();
      }

      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
      });
      const { recording } = await Audio.Recording.createAsync(
        Audio.RecordingOptionsPresets.HIGH_QUALITY
      );
      setRecording(recording);
      setIsRecording(true);
      console.log("Recording started...");

      await recording.startAsync();
    } catch (error) {
      console.log("Failed to start recording:", error);
    }
  };

  const stopRecording = async () => {
    if (!recording) return;

    try {
      await recording.stopAndUnloadAsync();
      setIsRecording(false);
      const uri = recording.getURI();
      console.log("Recording stopped. URI:", uri);

      if (uri) {
        setAudioUri(uri);

        // Suggest downloading the recording
        Alert.alert(
          "Recording Stopped",
          "Would you like to download your recording?",
          [
            {
              text: "Yes",
              onPress: () => downloadRecording(uri),
            },
            {
              text: "No",
              style: "cancel",
            },
          ]
        );
      }
    } catch (error) {
      console.log("Failed to stop recording:", error);
    }
  };

  const downloadRecording = async (uri: string) => {
    try {
      const fileUri = FileSystem.documentDirectory + "recording.mp3";

      await FileSystem.copyAsync({
        from: uri,
        to: fileUri,
      });

      console.log("File copied to:", fileUri);

      // Now suggest sharing the file
      Sharing.shareAsync(fileUri);
    } catch (error) {
      console.log("Error downloading the file:", error);
      Alert.alert(
        "Download failed",
        "There was an error downloading the file."
      );
    }
  };

  return (
    <View style={styles.container}>
      <Link href="/select" style={styles.goBackLink}>
        <Text>Go Back</Text>
      </Link>
      <Text style={styles.title}>😎 Vibe Coach 🎙️</Text>
      <Text style={styles.status}>
        {isRecording ? "Recording..." : "Tap to record 👇"}
      </Text>
      <Button
        mode="contained"
        style={styles.button}
        onPress={isRecording ? stopRecording : startRecording}
      >
        {isRecording ? "Stop Recording" : "Start Recording"}
      </Button>
      {audioUri && (
        <Text style={styles.audioText}>Recording saved at: {audioUri}</Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#f5f5f5",
    padding: 20,
  },
  goBackLink: {
    position: "absolute", // Absolute position to place it at the top left
    top: 70,
    left: 20,
    fontSize: 18,
    color: "#6200ee", // Blue color for the link
    fontWeight: "bold",
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 20,
  },
  status: {
    fontSize: 18,
    marginBottom: 20,
    color: "#333",
  },
  button: {
    padding: 10,
    borderRadius: 10,
    backgroundColor: "#6200ee",
  },
  audioText: {
    marginTop: 20,
    fontSize: 14,
    color: "#555",
  },
});
