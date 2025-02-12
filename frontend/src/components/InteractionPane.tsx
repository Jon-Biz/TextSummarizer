import React from 'react'
import ReactMarkdown from 'react-markdown'
import { Transcript, Summary } from '../types'

interface InteractionPaneProps {
  currentTranscript: Transcript | null
  currentSummary: Summary | null
}

const InteractionPane: React.FC<InteractionPaneProps> = ({
  currentTranscript,
  currentSummary,
}) => {
  return (
    <div className="flex-1 p-4">
      {currentSummary ? (
        <div>
          <h2 className="text-2xl font-bold">{currentSummary.title}</h2>
          <div className="mt-4 prose">
            <ReactMarkdown>{currentSummary.content}</ReactMarkdown>
          </div>
        </div>
      ) : (
        <p>No summary selected.</p>
      )}
    </div>
  )
}

export default InteractionPane