import React from 'react'
import { Transcript, Summary } from '../types'

interface PreviousItemsProps {
  transcripts: Transcript[]
  summaries: Summary[]
  onItemClick: (transcript: Transcript, summary: Summary) => void
}

const PreviousItems: React.FC<PreviousItemsProps> = ({
  transcripts,
  summaries,
  onItemClick,
}) => {
  return (
    <div className="p-4">
      <h3 className="text-lg font-bold mb-2">Previous Items</h3>
      <ul>
        {transcripts.map((transcript, index) => (
          <li key={transcript.id} className="mb-2">
            <button
              onClick={() => onItemClick(transcript, summaries[index])}
              className="text-blue-500 hover:underline"
            >
              {transcript.title}
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default PreviousItems