import React, { useState } from 'react'
import { Transcript, Summary } from '../types'
import { CurrentItemPane, PreviousItems } from './'

interface SidebarProps {
  transcripts: Transcript[]
  summaries: Summary[]
  currentTranscript: Transcript | null
  currentSummary: Summary | null
  onUpload: (file: File) => void
  onSettingsClick: () => void
  onItemClick: (transcript: Transcript, summary: Summary) => void
}

const Sidebar: React.FC<SidebarProps> = ({
  transcripts,
  summaries,
  currentTranscript,
  currentSummary,
  onUpload,
  onSettingsClick,
  onItemClick,
}) => {
  const handleItemClick = (transcript: Transcript, summary: Summary) => {
    onItemClick(transcript, summary)
  }

  return (
    <div className="w-64 bg-gray-200 p-4">
      <CurrentItemPane
        currentTranscript={currentTranscript}
        currentSummary={currentSummary}
      />
      <PreviousItems
        transcripts={transcripts}
        summaries={summaries}
        onItemClick={handleItemClick}
      />
      <div className="mt-4">
        <input
          type="file"
          accept="audio/*"
          onChange={(e) => {
            if (e.target.files) {
              onUpload(e.target.files[0])
            }
          }}
          className="w-full mb-2"
        />
        <button
          onClick={onSettingsClick}
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Settings
        </button>
      </div>
    </div>
  )
}

export default Sidebar