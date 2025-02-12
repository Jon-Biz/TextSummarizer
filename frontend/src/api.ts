import { Transcript, Summary, Settings } from './types'

export const fetchData = async () => {
  // Fetch transcripts, summaries, and settings from backend
  const transcripts: Transcript[] = []
  const summaries: Summary[] = []
  const settings: Settings = {
    systemPrompt: '',
    openaiApiKey: '',
    openaiEndpoint: '',
  }

  return { transcripts, summaries, settings }
}

export const uploadAudio = async (file: File) => {
  // Upload audio file to backend for processing
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch('/api/transcribe', {
    method: 'POST',
    body: formData,
  })

  if (!response.ok) {
    throw new Error('Failed to transcribe audio')
  }

  const { transcript_path } = await response.json()

  const transcriptResponse = await fetch(transcript_path)
  const transcriptContent = await transcriptResponse.text()

  const transcript: Transcript = {
    id: transcript_path.split('/').pop()!,
    title: '',
    content: transcriptContent,
  }

  const summaryResponse = await fetch('/api/summarize', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ transcript: transcriptContent }),
  })

  if (!summaryResponse.ok) {
    throw new Error('Failed to summarize transcript')
  }

  const { summary_path } = await summaryResponse.json()

  const summaryContentResponse = await fetch(summary_path)
  const summaryContent = await summaryContentResponse.text()

  const summary: Summary = {
    id: summary_path.split('/').pop()!,
    title: summaryContent.split('\n')[0].slice(2),
    content: summaryContent.split('\n').slice(1).join('\n'),
  }

  return { transcript, summary }
}

export const updateSettings = async (settings: Settings) => {
  const response = await fetch('/api/settings', {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(settings),
  })

  if (!response.ok) {
    throw new Error('Failed to update settings')
  }
}