export interface Transcript {
  id: string
  title: string
  content: string
}

export interface Summary {
  id: string
  title: string
  content: string
}

export interface Settings {
  systemPrompt: string
  openaiApiKey: string
  openaiEndpoint: string
}