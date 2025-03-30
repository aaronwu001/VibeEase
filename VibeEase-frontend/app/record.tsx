import React, { useState } from "react";
import { View, Text, Alert, StyleSheet } from "react-native";
import { Audio } from "expo-av";
import * as FileSystem from "expo-file-system";
import * as Sharing from "expo-sharing";
import { Button } from "react-native-paper";
import { Link } from "expo-router"; // Import Link from expo-router

export default function Record({ navigation }: any) {
  const [hasPermission, setHasPermission] = useState(false);
  const [recording, setRecording] = useState<Audio.Recording | null>(null);
  const [isRecording, setIsRecording] = useState(false);
  const [audioUri, setAudioUri] = useState<string | null>(null);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const userId1 = "67e8259487c915a2c5841751";
  const userId2 = "67e82599a7a20b37bda740fd";

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
      const jsonData = {
        user_id: userId1,
        other_user_id: userId2,
      };

      const response = await fetch("http://127.0.0.1:5000/start_conversation", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(jsonData),
      });

      console.log(response);

      if (response.ok) {
        Alert.alert("Successfully started a conversation");
      } else {
        Alert.alert(
          "Conversation pairing failed",
          "There was an error starting a conversation."
        );
        return;
      }

      const data = await response.json();

      const conversationId = data.conversation_id; // Extract the conversation_id
      console.log("Conversation ID:", conversationId);

      setConversationId(conversationId);

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

    if (!conversationId) return;

    const jsonData = {
      conversation_id: conversationId,
    };

    const response = await fetch("http://127.0.0.1:5000/end_conversation", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(jsonData),
    });

    try {
      await recording.stopAndUnloadAsync();
      setIsRecording(false);
      const uri = recording.getURI();
      console.log("Recording stopped. URI:", uri);

      if (uri) {
        setAudioUri(uri);

        // Upload the file to the server (may not be in mp3)
        uploadToAPI(uri);
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

      // Extract the file extension from the URI
      const fileExtension = blob.type.split("/").pop() || "mp3"; // Default to 'mp3' if no extension

      // Append the file Blob to the FormData with the correct filename
      formData.append("new_dialogue", blob, `recording.${fileExtension}`);
      formData.append("conversation_id", "fake_conversation_id");

      console.log("trying to upload to API now");

      const response = await fetch(
        "http://127.0.0.1:5000/update_conversation",
        {
          method: "POST",
          body: formData,
        }
      );

      console.log(response);

      if (response.ok) {
        const text = await response.text();
        Alert.alert("Success", `Transcription: ${text}`);
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
