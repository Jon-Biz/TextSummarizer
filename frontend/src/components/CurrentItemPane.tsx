import React from 'react'
import { Transcript, Summary } from '../types'

interface CurrentItemPaneProps {
  currentTranscript: Transcript | null
  currentSummary: Summary | null
}

const CurrentItemPane: React.FC<CurrentItemPaneProps> = ({
  currentTranscript,
  currentSummary,
}) => {
  return (
    <div className="p-4 bg-gray-100">
      <h3 className="text-lg font-bold mb-2">Current Item</h3>
      {currentTranscript && (
        <a
          href={`/transcripts/${currentTranscript.id}`}
          className="block text-blue-500 hover:underline"
        >
          Transcript
        </a>
      )}
      {currentSummary && (
        <a
          href={`/summaries/${currentSummary.id}`}
          className="block text-blue-500 hover:underline"
        >
          Summary
        </a>
      )}
    </div>
  )
}

export default CurrentItemPane