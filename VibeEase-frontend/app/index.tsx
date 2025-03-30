import React, { useState } from "react";
import { View, Text, Alert, StyleSheet } from "react-native";
import { Audio } from "expo-av";
import * as FileSystem from "expo-file-system";
import * as Sharing from "expo-sharing";
import { Button } from "react-native-paper";

export default function Index() {
  const [hasPermission, setHasPermission] = useState(false);
  const [recording, setRecording] = useState<Audio.Recording | null>(null);
  const [isRecording, setIsRecording] = useState(false);
  const [audioUri, setAudioUri] = useState<string | null>(null);

  const requestPermissions = async () => {
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
      if (!hasPermission) {
        await requestPermissions();
        if (!hasPermission) return;
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
        const fileName = `recording-${Date.now()}.mp3`;
        const newFileUri = FileSystem.documentDirectory + fileName;

        await FileSystem.moveAsync({ from: uri, to: newFileUri });
        console.log("File saved as MP3:", newFileUri);

        // Upload the MP3 file to an external API
        uploadToAPI(newFileUri);

        // if (await Sharing.isAvailableAsync()) {
        //   await Sharing.shareAsync(newFileUri);
        // } else {
        //   Alert.alert("Sharing not available on this device.");
        // }
      }
    } catch (error) {
      console.log("Failed to stop recording:", error);
    }
  };

  const uploadToAPI = async (fileUri: string) => {
    const formData = new FormData();

    try {
      // Fetch the file as a Blob
      const fileBlob = await fetch(fileUri);
      const blob = await fileBlob.blob();

      // Append the file Blob to the FormData
      formData.append("file", blob, "recording.mp3");

      //TODO: change the api endpoint
      const response = await fetch("https://your-api-endpoint.com/upload", {
        method: "POST",
        body: formData,
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      if (response.ok) {
        Alert.alert("File uploaded successfully!");
      } else {
        Alert.alert("Upload failed", "There was an error uploading the file.");
      }
    } catch (error) {
      console.log("Upload error:", error);
      Alert.alert("Upload failed", "Network error occurred.");
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>🎙️ Voice Recorder</Text>
      <Text style={styles.status}>
        {isRecording ? "Recording..." : "Tap to record"}
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
