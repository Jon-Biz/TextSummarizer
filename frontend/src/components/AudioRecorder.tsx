import React, { useState, useRef } from 'react';
import { ReactMic } from 'react-mic';
import axios, { AxiosError } from 'axios';

interface AudioRecorderProps {
  onTranscriptionUpdate: (partialTranscript: string) => void;
}

const AudioRecorder: React.FC<AudioRecorderProps> = ({ onTranscriptionUpdate }) => {
  const [recording, setRecording] = useState(false);
  const [audioChunks, setAudioChunks] = useState<Blob[]>([]);
  const eventSource = useRef<EventSource | null>(null);

  const startRecording = () => {
    setRecording(true);
    setAudioChunks([]);
  };

  const stopRecording = () => {
    setRecording(false);
  };

  const onData = (recordedBlob: Blob) => {
    setAudioChunks((prevChunks) => [...prevChunks, recordedBlob]);
  };

  const onStop = () => {
    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
    const formData = new FormData();
    formData.append('file', audioBlob, 'audio.wav');

    eventSource.current = new EventSource('/api/transcribe');
    eventSource.current.onmessage = (event) => {
      if (event.data === '[DONE]') {
        eventSource.current?.close();
      } else {
        onTranscriptionUpdate(event.data);
      }
    };

    axios
      .post('http://localhost:8000/api/transcribe', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        responseType: 'stream',
      })
      .catch((error: AxiosError) => {
        console.error('Error transcribing audio:', error);
      });
  };

  return (
    <div>
      <ReactMic
        record={recording}
        className="sound-wave"
        onStop={onStop}
        onData={onData}
        strokeColor="#000000"
        backgroundColor="#FF4081"
      />
      <button onClick={recording ? stopRecording : startRecording}>
        {recording ? 'Stop Recording' : 'Start Recording'}
      </button>
    </div>
  );
};

export default AudioRecorder;