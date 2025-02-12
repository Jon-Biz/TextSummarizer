import React, { useState, useEffect } from 'react'
import { Sidebar, InteractionPane, ProgressModal, SettingsModal } from './components'
import { fetchData, uploadAudio, updateSettings } from './api'
import { Transcript, Summary, Settings } from './types'

function App() {
  const [transcripts, setTranscripts] = useState<Transcript[]>([])
  const [summaries, setSummaries] = useState<Summary[]>([])
  const [currentTranscript, setCurrentTranscript] = useState<Transcript | null>(null)
  const [currentSummary, setCurrentSummary] = useState<Summary | null>(null)
  const [settings, setSettings] = useState<Settings | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [isSettingsOpen, setIsSettingsOpen] = useState(false)

  useEffect(() => {
    fetchData()
      .then(({ transcripts, summaries, settings }) => {
        setTranscripts(transcripts)
        setSummaries(summaries)
        setSettings(settings)
      })
      .catch(console.error)
  }, [])

  const handleUpload = async (file: File) => {
    setIsProcessing(true)
    try {
      const { transcript, summary } = await uploadAudio(file)
      setCurrentTranscript(transcript)
      setCurrentSummary(summary)
      setTranscripts([...transcripts, transcript])
      setSummaries([...summaries, summary])
    } catch (error) {
      console.error('Error uploading audio:', error)
    } finally {
      setIsProcessing(false)
    }
  }

  const handleSettingsChange = (newSettings: Settings) => {
    setSettings(newSettings)
    updateSettings(newSettings)
  }

  return (
    <div className="flex h-screen">
      <Sidebar
        transcripts={transcripts}
        summaries={summaries}
        currentTranscript={currentTranscript}
        currentSummary={currentSummary}
        onUpload={handleUpload}
        onSettingsClick={() => setIsSettingsOpen(true)}
        onItemClick={(transcript, summary) => {
          setCurrentTranscript(transcript)
          setCurrentSummary(summary)
        }}
      />
      <InteractionPane
        currentTranscript={currentTranscript}
        currentSummary={currentSummary}
      />
      {isProcessing && <ProgressModal />}
      {isSettingsOpen && (
        <SettingsModal
          settings={settings}
          onClose={() => setIsSettingsOpen(false)}
          onSettingsChange={handleSettingsChange}
        />
      )}
    </div>
  )
}

export default App
